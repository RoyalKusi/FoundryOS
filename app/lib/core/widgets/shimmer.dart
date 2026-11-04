import 'package:flutter/material.dart';

/// Three-dot shimmer for streaming per §5.9 — 8pt rise+fade 220ms
class StreamingShimmer extends StatefulWidget {
  const StreamingShimmer({super.key});
  @override
  State<StreamingShimmer> createState() => _S();
}

class _S extends State<StreamingShimmer> with SingleTickerProviderStateMixin {
  late final AnimationController _c = AnimationController(vsync: this, duration: const Duration(milliseconds: 900))..repeat();
  @override
  void dispose() { _c.dispose(); super.dispose(); }
  @override
  Widget build(BuildContext context) => AnimatedBuilder(
        animation: _c,
        builder: (_, __) => Row(mainAxisSize: MainAxisSize.min, children: List.generate(3, (i) {
          final t = (_c.value + i * 0.3) % 1.0;
          final opacity = 0.3 + 0.7 * (t < 0.5 ? t * 2 : (1 - t) * 2);
          return Padding(padding: const EdgeInsets.symmetric(horizontal: 2), child: Opacity(opacity: opacity, child: const CircleAvatar(radius: 4)));
        })),
      );
}

/// Message rise+fade — 8pt, 220ms (D3 perf)
class MessageBubble extends StatelessWidget {
  final Widget child;
  const MessageBubble({super.key, required this.child});
  @override
  Widget build(BuildContext context) => TweenAnimationBuilder(
        tween: Tween<Offset>(begin: const Offset(0, 0.02), end: Offset.zero),
        duration: const Duration(milliseconds: 220),
        curve: Curves.easeOut,
        builder: (_, o, c) => Transform.translate(offset: Offset(0, o.dy * 8), child: AnimatedOpacity(opacity: 1, duration: const Duration(milliseconds: 220), child: c)),
        child: child,
      );
}
