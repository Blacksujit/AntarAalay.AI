'use client';

import React from 'react';
import { snapAngle, normalizeAngle } from './compassUtils';

type Props = {
  angle: number;
  disabled?: boolean;
  onChange: (angle: number) => void;
  onSnap: () => void;
};

export function DirectionSelector({ angle, disabled = false, onChange, onSnap }: Props) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <button
        type="button"
        disabled={disabled}
        onClick={() => onChange(normalizeAngle(angle - 5))}
        className="px-3 py-2 rounded-lg border border-[#C6A75E]/30 bg-white text-[#1F1F1F] text-sm disabled:opacity-50"
      >
        -5°
      </button>
      <button
        type="button"
        disabled={disabled}
        onClick={() => onChange(normalizeAngle(angle + 5))}
        className="px-3 py-2 rounded-lg border border-[#C6A75E]/30 bg-white text-[#1F1F1F] text-sm disabled:opacity-50"
      >
        +5°
      </button>
      <button
        type="button"
        disabled={disabled}
        onClick={() => onChange(snapAngle(angle, 90))}
        className="px-3 py-2 rounded-lg border border-[#C6A75E]/30 bg-white text-[#1F1F1F] text-sm disabled:opacity-50"
      >
        Snap 90°
      </button>
      <button
        type="button"
        disabled={disabled}
        onClick={onSnap}
        className="px-3 py-2 rounded-lg bg-[#1F1F1F] text-white text-sm disabled:opacity-50"
      >
        Snap to Cardinals
      </button>
    </div>
  );
}
