import 'package:flutter/material.dart';
import 'package:el_4th_sem_fixed/EL_4TH_SEM/file.dart';
void main(){
  runApp(SpamCallDetection());
}
class  SpamCallDetection extends StatelessWidget{
  const SpamCallDetection({super.key});

  @override
  Widget build(BuildContext context){
    return MaterialApp(
      home: File(),
      theme: ThemeData.dark(useMaterial3: true),
      );
  }
}