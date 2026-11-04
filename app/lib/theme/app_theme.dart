import 'package:flutter/material.dart';
import 'app_colors.dart';

class AppTheme {
  static ThemeData lightTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(seedColor: AppColors.accentLight, brightness: Brightness.light).copyWith(
      primary: AppColors.accentLight,
      secondary: AppColors.accentMid,
      surface: AppColors.bgElevatedLight,
      error: AppColors.danger,
    ),
    scaffoldBackgroundColor: AppColors.bgPrimaryLight,
    appBarTheme: const AppBarTheme(backgroundColor: AppColors.bgPrimaryLight, elevation: 0, scrolledUnderElevation: 0),
    cardTheme: CardThemeData(
      color: AppColors.bgElevatedLight,
      shape: ContinuousRectangleBorder(borderRadius: BorderRadius.circular(28)),
      elevation: 0,
      margin: EdgeInsets.zero,
    ),
    dividerColor: AppColors.separatorLight,
  );
  static ThemeData darkTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(seedColor: AppColors.accentDark, brightness: Brightness.dark),
    scaffoldBackgroundColor: AppColors.bgPrimaryDark,
    appBarTheme: const AppBarTheme(backgroundColor: AppColors.bgPrimaryDark, elevation: 0),
  );
}
