import 'package:flutter/material.dart';
import '../../widgets/empty_state.dart';
import '../../widgets/app_logo.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      slivers: [
        SliverAppBar.large(
          title: const Row(children: [AppLogo(size: 32), SizedBox(width: 10), Text('FoundryOS')]),
        ),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(
                children: [
                  const AppLogo(size: 40, showWordmark: true),
                  const Spacer(),
                  // LIVE indicator — shows Baseten Maverick connection (set via --dart-define)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    decoration: BoxDecoration(
                      color: const String.fromEnvironment('BASETEN_API_KEY').isNotEmpty ||
                              const String.fromEnvironment('LLM_MODE') == 'live'
                          ? Colors.green.withOpacity(0.12)
                          : Theme.of(context).colorScheme.primary.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(
                        color: const String.fromEnvironment('BASETEN_API_KEY').isNotEmpty
                            ? Colors.green.withOpacity(0.3)
                            : Colors.transparent,
                        width: 1,
                      ),
                    ),
                    child: Row(mainAxisSize: MainAxisSize.min, children: [
                      Icon(
                        const String.fromEnvironment('BASETEN_API_KEY').isNotEmpty ? Icons.cloud_done_outlined : Icons.cloud_off_outlined,
                        size: 14,
                        color: const String.fromEnvironment('BASETEN_API_KEY').isNotEmpty ? Colors.green.shade700 : Theme.of(context).colorScheme.primary,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        const String.fromEnvironment('BASETEN_API_KEY').isNotEmpty ? 'LIVE • Maverick 17B' : 'MOCK • No keys needed',
                        style: Theme.of(context).textTheme.labelSmall?.copyWith(
                              color: const String.fromEnvironment('BASETEN_API_KEY').isNotEmpty ? Colors.green.shade700 : Theme.of(context).colorScheme.primary,
                              fontWeight: FontWeight.w600,
                            ),
                      ),
                    ]),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Text('Good morning, Founder — ${DateTime.now().toString().split(' ')[0]}',
                  style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: 12),
              Card(child: ListTile(title: const Text('Today'), subtitle: const Text('Top 3 priorities will appear here'))),
              const SizedBox(height: 12),
              Card(child: ListTile(title: const Text('Approvals waiting'), trailing: Chip(label: Text('0')))),
              const SizedBox(height: 12),
              const EmptyState(title: 'No reports yet', body: 'Role reports will appear as cards.'),
              const SizedBox(height: 12),
              TextField(decoration: InputDecoration(hintText: 'Ask your company…', border: OutlineInputBorder(borderRadius: BorderRadius.circular(28)))),
            ]),
          ),
        ),
      ],
    );
  }
}
