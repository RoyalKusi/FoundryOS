import 'package:flutter/material.dart';
import '../../widgets/app_logo.dart';

class GenesisScreen extends StatelessWidget {
  const GenesisScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Row(children: [AppLogo(size: 28), SizedBox(width: 8), Text('FoundryOS')]), centerTitle: false),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
            const AppLogo(size: 96, showWordmark: true),
            const SizedBox(height: 24),
            Text('Welcome to FoundryOS', style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 8),
            Text('Turn your idea into a Company OS staffed by digital employees who do real work.',
                textAlign: TextAlign.center, style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: Colors.grey)),
            const SizedBox(height: 24),
            TextFormField(decoration: const InputDecoration(labelText: 'Company name')),
            const SizedBox(height: 12),
            TextFormField(decoration: const InputDecoration(labelText: 'Pitch')),
            const SizedBox(height: 12),
            FilledButton(onPressed: () {}, child: const Text('Generate Charter')),
            const SizedBox(height: 12),
            TextButton(onPressed: () {}, child: const Text('Preview with Mock Data')),
          ]),
        ),
      ),
    );
  }
}
