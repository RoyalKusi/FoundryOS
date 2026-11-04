import 'package:flutter/material.dart';

class ApprovalSheet extends StatelessWidget {
  final String title;
  final String rationale;
  const ApprovalSheet({super.key, required this.title, required this.rationale});
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        Text(title, style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 8),
        Text(rationale),
        const SizedBox(height: 12),
        Row(children: [
          Expanded(child: FilledButton(onPressed: () {}, child: const Text('Approve'))),
          const SizedBox(width: 8),
          Expanded(child: OutlinedButton(onPressed: () {}, child: const Text('Reject'))),
        ])
      ]),
    );
  }
}
