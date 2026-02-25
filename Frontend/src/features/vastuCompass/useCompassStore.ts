'use client';

import { create } from 'zustand';
import { angleToMappedDirections, normalizeAngle, type Cardinal } from './compassUtils';

type MappedDirections = Record<Cardinal, Cardinal>;

interface CompassState {
  angle: number;
  mappedDirections: MappedDirections;
  confirmed: boolean;
  lastUpdated: string;

  setAngle: (angle: number) => void;
  confirm: () => void;
  reset: () => void;
}

const nowIso = () => new Date().toISOString();

export const useCompassStore = create<CompassState>((set, get) => ({
  angle: 0,
  mappedDirections: angleToMappedDirections(0),
  confirmed: false,
  lastUpdated: nowIso(),

  setAngle: (angle: number) => {
    if (get().confirmed) return;
    const normalized = normalizeAngle(angle);
    set({
      angle: normalized,
      mappedDirections: angleToMappedDirections(normalized),
      lastUpdated: nowIso(),
    });
  },

  confirm: () => {
    set({ confirmed: true, lastUpdated: nowIso() });
  },

  reset: () => {
    set({
      angle: 0,
      mappedDirections: angleToMappedDirections(0),
      confirmed: false,
      lastUpdated: nowIso(),
    });
  },
}));
