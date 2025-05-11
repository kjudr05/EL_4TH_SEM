import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class MakePhoneCall extends StatefulWidget {
  const MakePhoneCall({super.key});

  @override
  State<MakePhoneCall> createState() => MakePhoneCallState();
}

class MakePhoneCallState extends State<MakePhoneCall> {
  String _input = '';

  void _onKeyTap(String value) {
    setState(() {
      _input += value;
    });
  }

  void _onBackspace() {
    setState(() {
      if (_input.isNotEmpty) {
        _input = _input.substring(0, _input.length - 1);         //substring(start, end) returns the part of the string from start to end - 1.
      }
    });
  }
 /*Uri(scheme: 'tel', path: _input) creates a URI like:
tel:9876543210

canLaunchUrl() checks if the device can open this URI.

launchUrl() opens the dialer or makes the call if it’s possible*/
  void _makeCall() async {
    final Uri phoneUri = Uri(scheme: 'tel', path: _input);
    if (await canLaunchUrl(phoneUri)) {
      await launchUrl(phoneUri);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Cannot make the call')),
      );
    }
  }

  Widget _buildDialButton(String number) {
  return Container(
    decoration: BoxDecoration(
      shape: BoxShape.circle,
      border: Border.all(color: Colors.white, width: 2), // Optional border for visibility
    ),
    child: ElevatedButton(
      onPressed: () => _onKeyTap(number),
      style: ElevatedButton.styleFrom(
        shape: const CircleBorder(),
        padding: const EdgeInsets.all(24),
        backgroundColor: Colors.deepPurple,
        elevation: 4,
      ),
      child: Text(
        number,
        style: const TextStyle(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
    ),
  );
}


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Dial Pad"),
        backgroundColor: Colors.deepPurple,
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            Text(
              _input,
              style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            Column(
  children: [
    Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _buildDialButton('1'),
        _buildDialButton('2'),
        _buildDialButton('3'),
      ],
    ),
    const SizedBox(height: 20),
    Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _buildDialButton('4'),
        _buildDialButton('5'),
        _buildDialButton('6'),
      ],
    ),
    const SizedBox(height: 20),
    Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _buildDialButton('7'),
        _buildDialButton('8'),
        _buildDialButton('9'),
      ],
    ),
    const SizedBox(height: 20),
    Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _buildDialButton('*'),
        _buildDialButton('0'),
        _buildDialButton('#'),
      ],
    ),
  ],
),

            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                IconButton(
                  icon: const Icon(Icons.backspace, color: Colors.red),
                  onPressed: _onBackspace,
                ),
                ElevatedButton.icon(
                  onPressed: _makeCall,
                  icon: const Icon(Icons.call),
                  label: const Text("Call"),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                  ),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}