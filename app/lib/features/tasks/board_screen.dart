import 'package:flutter/material.dart';
import '../../widgets/empty_state.dart';
class BoardScreen extends StatelessWidget {
  const BoardScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return CustomScrollView(slivers: [
      const SliverAppBar.large(title: Text('Tasks')),
      SliverFillRemaining(child: EmptyState(title: 'No tasks', body: 'Tasks from meetings and agents will appear here.')),
    ]);
  }
}
