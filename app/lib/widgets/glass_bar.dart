import 'dart:ui';
import 'package:flutter/material.dart';

class GlassBar extends StatelessWidget {
  final Widget child;
  final double height;
  const GlassBar({super.key, required this.child, this.height = 56});

  @override
  Widget build(BuildContext context) {
    final isHighContrast = MediaQuery.of(context).highContrast;
    if (isHighContrast) {
      return Container(height: height, color: Theme.of(context).colorScheme.surface, child: child);
    }
    return ClipRect(
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 24, sigmaY: 24),
        child: Container(
          height: height,
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surface.withOpacity(0.72),
            border: Border(top: BorderSide(color: Theme.of(context).dividerColor.withOpacity(0.2), width: 0.5)),
          ),
          child: child,
        ),
      ),
    );
  }
}
