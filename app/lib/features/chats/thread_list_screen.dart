import 'package:flutter/material.dart';
import '../../widgets/empty_state.dart';
class ThreadListScreen extends StatelessWidget {
  const ThreadListScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return CustomScrollView(slivers: [
      const SliverAppBar.large(title: Text('Chats')),
      SliverFillRemaining(child: EmptyState(title: 'No chats', body: 'Start a thread with any role.', actionLabel: 'New chat', onAction: () {})),
    ]);
  }
}
