import 'package:flutter/material.dart';

class BoardScreen extends StatefulWidget {
  const BoardScreen({super.key});
  @override
  State<BoardScreen> createState() => _B();
}

class _B extends State<BoardScreen> {
  final _columns = {
    'todo': ['Ship MVP', 'Onboard 10 pilots'],
    'doing': ['RAG evals'],
    'done': ['Brand kit'],
  };
  @override
  Widget build(BuildContext context) {
    return CustomScrollView(slivers: [
      const SliverAppBar.large(title: Text('Tasks')),
      SliverToBoxAdapter(
        child: SizedBox(height: 420, child: Row(children: _columns.entries.map((e) => Expanded(child: Column(children: [Chip(label: Text(e.key)), Expanded(child: ListView.builder(itemCount: e.value.length, itemBuilder: (c, i) => Card(margin: const EdgeInsets.all(6), child: ListTile(title: Text(e.value[i]), subtitle: const Text('Drag to move — optimistic'))))))]))).toList())),
      ),
    ]);
  }
}
