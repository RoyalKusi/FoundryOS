import 'package:flutter/material.dart';

abstract class AppColors {
  // Light — per §5.3 Tokens
  static const bgPrimaryLight = Color(0xFFFFFFFF);
  static const bgSecondaryLight = Color(0xFFF5F5F7);
  static const bgElevatedLight = Color(0xFFFFFFFF);
  static const labelPrimaryLight = Color(0xFF1D1D1F);
  static const labelSecondaryLight = Color(0xFF6E6E73);
  static const labelTertiaryLight = Color(0xFF9A9AA0);
  static const separatorLight = Color(0x2E3C3C43);
  static const accentLight = Color(0xFF4F46E5);
  static const accentMid = Color(0xFF6366F1);
  // Dark
  static const bgPrimaryDark = Color(0xFF000000);
  static const bgSecondaryDark = Color(0xFF0B0B0D);
  static const bgElevatedDark = Color(0xFF1C1C1E);
  static const labelPrimaryDark = Color(0xFFF5F5F7);
  static const labelSecondaryDark = Color(0xFF9A9AA0);
  static const accentDark = Color(0xFF7C74FF);
  // Semantic
  static const success = Color(0xFF34C759);
  static const warning = Color(0xFFFF9F0A);
  static const danger = Color(0xFFFF3B30);
  static const aiTint = Color(0x195E5CE6);
  static const aiTintDark = Color(0x295E5CE6);
  static const humanTint = Color(0x190A84FF);
  static const humanTintDark = Color(0x290A84FF);

  // Gradients
  static const foundryGradientLight = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF4F46E5), Color(0xFF6366F1), Color(0xFF7C74FF)],
  );
  static const foundryGradientDark = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF6366F1), Color(0xFF7C74FF), Color(0xFF8B85FF)],
  );
}
