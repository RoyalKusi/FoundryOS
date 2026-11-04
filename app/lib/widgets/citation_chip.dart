import 'package:flutter/material.dart';

class CitationChip extends StatelessWidget {
  final String citationId;
  const CitationChip({super.key, required this.citationId});
  @override
  Widget build(BuildContext context) {
    return Chip(label: Text('[c:$citationId]'), visualDensity: VisualDensity.compact);
  }
}
