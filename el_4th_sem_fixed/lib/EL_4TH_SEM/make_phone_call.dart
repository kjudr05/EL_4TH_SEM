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
        _input = _input.substring(0, _input.length - 1);
      }
    });
  }

  Future<void> _makeCall() async {
    if (_input.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please enter a number.")),
      );
      return;
    }

    final Uri phoneUri = Uri(scheme: 'tel', path: _input);

    if (await canLaunchUrl(phoneUri)) {
      await launchUrl(phoneUri, mode: LaunchMode.externalApplication); // Opens the dialer
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Cannot launch the dialer.')),
      );
    }
  }

  Widget _buildDialButton(String number) {
    return SizedBox(
      width: 70,
      height: 70,
      child: ElevatedButton(
        onPressed: () => _onKeyTap(number),
        style: ElevatedButton.styleFrom(
          shape: const CircleBorder(),
          backgroundColor: Colors.deepPurple,
          elevation: 4,
          padding: EdgeInsets.zero,
        ),
        child: Text(
          number == ' ' ? '_' : number, // Show _ for space visually
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
            const SizedBox(height: 30),
            Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [_buildDialButton('1'), _buildDialButton('2'), _buildDialButton('3')],
                ),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [_buildDialButton('4'), _buildDialButton('5'), _buildDialButton('6')],
                ),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [_buildDialButton('7'), _buildDialButton('8'), _buildDialButton('9')],
                ),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [_buildDialButton('*'), _buildDialButton('0'), _buildDialButton('#')],
                ),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildDialButton('+'),
                    _buildDialButton(' '), // Space
                    const SizedBox(width: 70), // Placeholder for layout symmetry
                  ],
                ),
              ],
            ),
            const SizedBox(height: 30),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                IconButton(
                  icon: const Icon(Icons.backspace, color: Colors.red),
                  iconSize: 30,
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
