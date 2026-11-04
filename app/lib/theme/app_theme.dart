import 'package:flutter/material.dart';
import 'app_colors.dart';

class AppTheme {
  static ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(seedColor: AppColors.accentLight, brightness: Brightness.light),
    scaffoldBackgroundColor: AppColors.bgPrimaryLight,
    appBarTheme: const AppBarTheme(backgroundColor: AppColors.bgPrimaryLight, elevation: 0),
  );
  static ThemeData darkTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(seedColor: AppColors.accentDark, brightness: Brightness.dark),
    scaffoldBackgroundColor: AppColors.bgPrimaryDark,
    appBarTheme: const AppBarTheme(backgroundColor: AppColors.bgPrimaryDark, elevation: 0),
  );
}
