import 'package:flutter/material.dart';

/// Global error boundary per §6 — catches unhandled, shows what happened + what to do
class ErrorBoundary extends StatefulWidget {
  final Widget child;
  const ErrorBoundary({super.key, required this.child});
  @override
  State<ErrorBoundary> createState() => _E();
}

class _E extends State<ErrorBoundary> {
  FlutterErrorDetails? _error;
  @override
  void initState() {
    super.initState();
    FlutterError.onError = (details) {
      setState(() => _error = details);
      FlutterError.presentError(details);
    };
  }

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      return MaterialApp(
        home: Scaffold(
          body: Center(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                const Icon(Icons.error_outline_rounded, size: 48, color: Colors.red),
                const SizedBox(height: 12),
                const Text('Something went wrong', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
                const SizedBox(height: 8),
                Text(_error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: Colors.grey)),
                const SizedBox(height: 16),
                FilledButton(onPressed: () => setState(() => _error = null), child: const Text('Try again')),
              ]),
            ),
          ),
        ),
      );
    }
    return widget.child;
  }
}
