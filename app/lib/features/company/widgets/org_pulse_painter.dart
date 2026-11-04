import 'package:flutter/material.dart';

class OrgPulsePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0x594F46E5)
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;
    final center = Offset(size.width / 2, size.height / 2);
    canvas.drawCircle(center, 40, paint);
    canvas.drawCircle(center, 70, paint..strokeWidth = 1);
    // Simple nodes
    final nodePaint = Paint()..color = const Color(0xFF4F46E5);
    canvas.drawCircle(Offset(center.dx, center.dy - 80), 20, nodePaint);
    canvas.drawCircle(Offset(center.dx - 60, center.dy + 40), 18, nodePaint);
    canvas.drawCircle(Offset(center.dx + 60, center.dy + 40), 18, nodePaint);
    // Lines
    final linePaint = Paint()..color = const Color(0x594F46E5)..strokeWidth = 2;
    canvas.drawLine(Offset(center.dx, center.dy - 60), Offset(center.dx - 50, center.dy + 25), linePaint);
    canvas.drawLine(Offset(center.dx, center.dy - 60), Offset(center.dx + 50, center.dy + 25), linePaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
