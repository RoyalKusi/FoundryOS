import 'package:flutter/material.dart';

class ScheduleScreen extends StatefulWidget {
  const ScheduleScreen({super.key});
  @override
  State<ScheduleScreen> createState() => _S();
}

class _S extends State<ScheduleScreen> {
  int _sel = 3;
  final _meetings = [
    {'title': 'Standup', 'time': '08:00', 'att': 'FO + Assistant'},
    {'title': 'Investor sync', 'time': '14:00', 'att': 'FO + CFO'},
  ];
  void _newMeeting() => showModalBottomSheet(context: context, isScrollControlled: true, builder: (_) => Padding(
        padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom, left: 16, right: 16, top: 16),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Text('New meeting', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
          TextFormField(decoration: const InputDecoration(labelText: 'Title')),
          TextFormField(decoration: const InputDecoration(labelText: 'Agenda')),
          const SizedBox(height: 12),
          FilledButton(onPressed: () { Navigator.pop(context); ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Meeting created → turn-by-turn + Resolutions drawer'))); }, child: const Text('Create')),
          const SizedBox(height: 16),
        ]),
      ));

  @override
  Widget build(BuildContext context) {
    return CustomScrollView(slivers: [
      const SliverAppBar.large(title: Text('Schedule')),
      SliverToBoxAdapter(child: SizedBox(height: 72, child: ListView.builder(scrollDirection: Axis.horizontal, itemCount: 7, itemBuilder: (c, i) => GestureDetector(onTap: () => setState(() => _sel = i), child: Container(margin: const EdgeInsets.all(8), padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8), decoration: BoxDecoration(color: _sel == i ? Theme.of(context).colorScheme.primary : Theme.of(context).colorScheme.surfaceContainerHighest, borderRadius: BorderRadius.circular(14)), child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [Text(['M', 'T', 'W', 'T', 'F', 'S', 'S'][i], style: TextStyle(color: _sel == i ? Colors.white : null)), Text('${i + 10}', style: TextStyle(color: _sel == i ? Colors.white : null))])))))),
      SliverPadding(
        padding: const EdgeInsets.all(12),
        sliver: SliverList.builder(itemCount: _meetings.length, itemBuilder: (c, i) => Card(child: ListTile(title: Text(_meetings[i]['title']!), subtitle: Text(_meetings[i]['att']!), trailing: Chip(label: Text(_meetings[i]['time']!)), onTap: () => ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Meeting room: agenda + turn-by-turn + Resolutions drawer → Confirm → timeline'))))),
      ),
      SliverToBoxAdapter(child: Padding(padding: const EdgeInsets.all(16), child: FilledButton(onPressed: _newMeeting, child: const Text('New meeting')))),
    ]);
  }
}
