import 'package:flutter/material.dart';
import 'router.dart';
import 'theme/app_theme.dart';

class FoundryApp extends StatelessWidget {
  const FoundryApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'FoundryOS',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      routerConfig: appRouter,
    );
  }
}
