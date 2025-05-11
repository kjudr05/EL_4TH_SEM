import 'package:flutter/material.dart';
import 'package:el_4th_sem_fixed/EL_4TH_SEM/login_page.dart';
import 'package:el_4th_sem_fixed/EL_4TH_SEM/second_page.dart';
import 'package:el_4th_sem_fixed/EL_4TH_SEM/make_phone_call.dart';


class File extends StatelessWidget {
  const File({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Spam Call Detection',
      initialRoute: '/',
      routes: {
        '/': (context) => const LoginPage(),
        '/dashboard': (context) => const SecondPage(),
        '/dialpad': (context) => const MakePhoneCall(),
      },
    );
  }
}