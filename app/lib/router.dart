import 'dart:ui';
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
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return Scaffold(
      body: navigationShell,
      // Glassmorphism tab bar per §5.5 + §5.9 — only tab bar, nav bar scrolled, composer, modal grabber
      bottomNavigationBar: ClipRect(
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 24, sigmaY: 24),
          child: Container(
            decoration: BoxDecoration(
              color: isDark ? const Color(0xAE1C1C1E) : const Color(0xB8FFFFFF), // 0.68 / 0.72
              border: Border(top: BorderSide(color: Colors.white.withOpacity(0.5), width: 0.5)),
            ),
            child: NavigationBar(
              backgroundColor: Colors.transparent,
              surfaceTintColor: Colors.transparent,
              indicatorColor: Theme.of(context).colorScheme.primary.withOpacity(0.12),
              selectedIndex: navigationShell.currentIndex,
              onDestinationSelected: navigationShell.goBranch,
              destinations: const [
                NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home_rounded), label: 'Home'),
                NavigationDestination(icon: Icon(Icons.chat_bubble_outline), selectedIcon: Icon(Icons.chat_bubble_rounded), label: 'Messages'),
                NavigationDestination(icon: Icon(Icons.calendar_today_outlined), selectedIcon: Icon(Icons.calendar_today_rounded), label: 'Schedule'),
                NavigationDestination(icon: Icon(Icons.approval_outlined), selectedIcon: Icon(Icons.approval), label: 'Approvals'),
                NavigationDestination(icon: Icon(Icons.hub_outlined), selectedIcon: Icon(Icons.hub_rounded), label: 'Company'),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
