import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:foundryos_app/app.dart';
import 'package:foundryos_app/widgets/app_logo.dart';

void main() {
  testWidgets('App smoke test - Home tab default', (tester) async {
    await tester.pumpWidget(const FoundryApp());
    expect(find.text('Home'), findsOneWidget);
  });

  testWidgets('AppLogo renders', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: Scaffold(body: AppLogo(size: 48, showWordmark: true))));
    expect(find.byType(AppLogo), findsOneWidget);
  });
}
