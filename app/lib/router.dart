import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'features/approvals/inbox_screen.dart';
import 'features/chats/thread_list_screen.dart';
import 'features/company/company_screen.dart';
import 'features/genesis/genesis_screen.dart';
import 'features/home/home_screen.dart';
import 'features/schedule/schedule_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/home',
  routes: [
    GoRoute(path: '/genesis', builder: (context, state) => const GenesisScreen()),
    StatefulShellRoute.indexedStack(
      builder: (context, state, navigationShell) => ScaffoldWithNav(navigationShell: navigationShell),
      branches: [
        StatefulShellBranch(routes: [GoRoute(path: '/home', builder: (context, state) => const HomeScreen())]),
        StatefulShellBranch(routes: [GoRoute(path: '/chats', builder: (context, state) => const ThreadListScreen())]),
        StatefulShellBranch(routes: [GoRoute(path: '/schedule', builder: (context, state) => const ScheduleScreen())]),
        StatefulShellBranch(routes: [GoRoute(path: '/approvals', builder: (context, state) => const InboxScreen())]),
        StatefulShellBranch(routes: [GoRoute(path: '/company', builder: (context, state) => const CompanyScreen())]),
      ],
    ),
  ],
);

class ScaffoldWithNav extends StatelessWidget {
  final StatefulNavigationShell navigationShell;
  const ScaffoldWithNav({super.key, required this.navigationShell});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: NavigationBar(
        selectedIndex: navigationShell.currentIndex,
        onDestinationSelected: navigationShell.goBranch,
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.chat_bubble_outline), label: 'Messages'),
          NavigationDestination(icon: Icon(Icons.calendar_today_outlined), label: 'Schedule'),
          NavigationDestination(icon: Icon(Icons.approval_outlined), label: 'Approvals'),
          NavigationDestination(icon: Icon(Icons.hub_outlined), label: 'Company'),
        ],
      ),
    );
  }
}
