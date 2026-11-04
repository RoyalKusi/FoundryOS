import 'package:flutter/material.dart';

class Avatar extends StatelessWidget {
  final String initials;
  final bool isAi;
  final double size;
  const Avatar({super.key, required this.initials, this.isAi = false, this.size = 40});
  @override
  Widget build(BuildContext context) {
    return Container(
      width: size, height: size,
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: isAi ? [const Color(0xFF4F46E5), const Color(0xFF7C74FF)] : [const Color(0xFF0A84FF), const Color(0xFF409CFF)]),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Center(child: Text(initials, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w700))),
    );
  }
}
