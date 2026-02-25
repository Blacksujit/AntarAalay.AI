'use client';

import dynamic from 'next/dynamic';
import React, { useMemo } from 'react';
import { useCompassStore } from './useCompassStore';
import { snapAngle } from './compassUtils';
import { DirectionSelector } from './DirectionSelector';

const CompassDial = dynamic(async () => {
  const mod = await import('./CompassDial');
  return mod.CompassDial;
}, { ssr: false });

export function VastuCompass() {
  const { angle, confirmed, setAngle, confirm, reset } = useCompassStore();

  const dialDisabled = confirmed;

  const helpText = useMemo(() => {
    return 'Rotate the compass so the arrow points to true North for your space, then lock orientation. This prevents north/south mix-ups and improves Vastu alignment.';
  }, []);

  return (
    <section className="mb-6 bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-[#1F1F1F]">Vastu Compass</h2>
          <p className="text-sm text-gray-600 mt-1">{helpText}</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => reset()}
            className="px-4 py-2 rounded-lg border border-[#C6A75E]/30 text-[#1F1F1F] text-sm"
          >
            Reset
          </button>
          <button
            type="button"
            disabled={confirmed}
            onClick={() => confirm()}
            className="px-4 py-2 rounded-lg bg-[#C6A75E] text-white text-sm disabled:opacity-60"
          >
            {confirmed ? 'Locked' : 'Lock Orientation'}
          </button>
        </div>
      </div>

      <div className="mt-6 flex flex-col md:flex-row gap-6 md:items-center">
        <div className="flex justify-center md:justify-start">
          <CompassDial angle={angle} disabled={dialDisabled} onChange={setAngle} />
        </div>
        <div className="flex-1 space-y-3">
          <div className="text-sm text-gray-700">
            <div className="font-medium">Orientation</div>
            <div className="mt-1">{Math.round(angle)}°</div>
          </div>

          <DirectionSelector
            angle={angle}
            disabled={dialDisabled}
            onChange={setAngle}
            onSnap={() => setAngle(snapAngle(angle, 90))}
          />

          {!confirmed && (
            <div className="text-xs text-gray-500">
              Tip: Use ArrowLeft/ArrowRight keys to rotate (Shift for bigger steps).
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
