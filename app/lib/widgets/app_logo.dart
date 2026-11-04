import 'package:flutter/material.dart';

/// FoundryOS Logo widget — uses branding assets with light/dark adaptive.
/// Shows squircle gradient + F + sparkle via SVG/PNG, falls back to painted version if asset missing.
class AppLogo extends StatelessWidget {
  final double size;
  final bool showWordmark;
  const AppLogo({super.key, this.size = 48, this.showWordmark = false});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        _IconSquircle(size: size, isDark: isDark),
        if (showWordmark) ...[
          const SizedBox(width: 12),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              RichText(
                text: TextSpan(
                  style: TextStyle(
                    fontSize: size * 0.42,
                    fontWeight: FontWeight.w700,
                    letterSpacing: -0.5,
                    color: isDark ? Colors.white : const Color(0xFF1D1D1F),
                  ),
                  children: [
                    const TextSpan(text: 'Foundry'),
                    TextSpan(
                      text: 'OS',
                      style: TextStyle(
                        fontWeight: FontWeight.w400,
                        color: isDark ? const Color(0xFF7C74FF) : const Color(0xFF4F46E5),
                      ),
                    ),
                  ],
                ),
              ),
              Text(
                'COMPANY OPERATING SYSTEM',
                style: TextStyle(
                  fontSize: 8,
                  fontWeight: FontWeight.w500,
                  letterSpacing: 1.2,
                  color: isDark ? const Color(0xFF9A9AA0) : const Color(0xFF6E6E73),
                ),
              ),
            ],
          ),
        ],
      ],
    );
  }
}

class _IconSquircle extends StatelessWidget {
  final double size;
  final bool isDark;
  const _IconSquircle({required this.size, required this.isDark});

  @override
  Widget build(BuildContext context) {
    // Try asset, fallback to painted
    return SizedBox(
      width: size,
      height: size,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(size * 0.27),
        child: Image.asset(
          'assets/branding/app_icon.png',
          fit: BoxFit.cover,
          errorBuilder: (_, __, ___) => _PaintedLogo(size: size),
        ),
      ),
    );
  }
}

class _PaintedLogo extends StatelessWidget {
  final double size;
  const _PaintedLogo({required this.size});

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: Size(size, size),
      painter: _LogoPainter(),
    );
  }
}

class _LogoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final r = size.width * 0.273 * 1.2;
    final rect = RRect.fromRectAndRadius(Offset.zero & size, Radius.circular(r));
    // gradient
    final gradient = const LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [Color(0xFF4F46E5), Color(0xFF6366F1), Color(0xFF7C74FF)],
    ).createShader(Offset.zero & size);
    canvas.drawRRect(rect, Paint()..shader = gradient);
    // highlight
    final hl = Paint()
      ..shader = LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
        colors: [Colors.white.withOpacity(0.18), Colors.transparent],
      ).createShader(Offset.zero & size);
    canvas.drawRRect(rect, hl);

    // F monogram — relative to size
    final fw = size.width * 0.48;
    final fh = size.height * 0.52;
    final fx = (size.width - fw) / 2;
    final fy = (size.height - fh) / 2;
    final th = fw * 0.18;
    final radius = Radius.circular(th * 0.2);

    final white = Paint()..color = Colors.white;

    // vertical
    canvas.drawRRect(
      RRect.fromRectAndRadius(Rect.fromLTWH(fx, fy, th, fh), radius),
      white,
    );
    // top
    canvas.drawRRect(
      RRect.fromRectAndRadius(Rect.fromLTWH(fx, fy, fw, th), radius),
      white,
    );
    // middle
    final midW = fw * 0.68;
    final midH = th * 0.88;
    final midY = fy + fh * 0.32;
    canvas.drawRRect(
      RRect.fromRectAndRadius(Rect.fromLTWH(fx, midY, midW, midH), radius),
      white,
    );

    // sparkle
    final sx = size.width * 0.78;
    final sy = size.height * 0.22;
    final s = size.width * 0.035;
    final sparkle = Path()
      ..moveTo(sx, sy - s)
      ..lineTo(sx + s * 0.25, sy - s * 0.25)
      ..lineTo(sx + s, sy)
      ..lineTo(sx + s * 0.25, sy + s * 0.25)
      ..lineTo(sx, sy + s)
      ..lineTo(sx - s * 0.25, sy + s * 0.25)
      ..lineTo(sx - s, sy)
      ..lineTo(sx - s * 0.25, sy - s * 0.25)
      ..close();
    // glow
    canvas.drawCircle(Offset(sx, sy), s * 1.6, Paint()..color = Colors.white.withOpacity(0.22));
    canvas.drawCircle(Offset(sx, sy), s * 1.25, Paint()..color = Colors.white.withOpacity(0.14));
    canvas.drawPath(sparkle, white);
    canvas.drawCircle(Offset(sx, sy), 3, white);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
