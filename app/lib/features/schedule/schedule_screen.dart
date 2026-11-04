import 'package:flutter/material.dart';
import '../../widgets/empty_state.dart';

class ScheduleScreen extends StatelessWidget {
  const ScheduleScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      slivers: [
        const SliverAppBar.large(title: Text('Schedule')),
        SliverToBoxAdapter(
          child: Column(children: [
            SizedBox(
              height: 60,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: 7,
                itemBuilder: (c, i) => Padding(
                  padding: const EdgeInsets.all(8),
                  child: Chip(label: Text('Day ${i + 1}')),
                ),
              ),
            ),
            const EmptyState(title: 'No events', body: 'Meetings, deadlines, cadences will appear here.'),
            FilledButton(onPressed: () {}, child: const Text('New meeting')),
          ]),
        ),
      ],
    );
  }
}
