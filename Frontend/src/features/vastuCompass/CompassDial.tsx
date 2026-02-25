'use client';

import React, { useCallback, useMemo, useRef, useState } from 'react';
import { normalizeAngle } from './compassUtils';

type Props = {
  angle: number;
  disabled?: boolean;
  onChange: (angle: number) => void;
};

function getAngleFromPointer(centerX: number, centerY: number, clientX: number, clientY: number): number {
  const dx = clientX - centerX;
  const dy = clientY - centerY;
  const rad = Math.atan2(dy, dx);
  const deg = (rad * 180) / Math.PI;
  return normalizeAngle(deg + 90);
}

export const CompassDial = React.memo(function CompassDial({ angle, disabled = false, onChange }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const style = useMemo(() => ({
    transform: `rotate(${angle}deg)`,
  }), [angle]);

  const updateFromEvent = useCallback((e: PointerEvent | React.PointerEvent) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    const clientX = 'clientX' in e ? e.clientX : 0;
    const clientY = 'clientY' in e ? e.clientY : 0;

    const next = getAngleFromPointer(cx, cy, clientX, clientY);
    onChange(next);
  }, [onChange]);

  const onPointerDown = useCallback((e: React.PointerEvent) => {
    if (disabled) return;
    (e.currentTarget as HTMLDivElement).setPointerCapture(e.pointerId);
    setIsDragging(true);
    updateFromEvent(e);
  }, [disabled, updateFromEvent]);

  const onPointerMove = useCallback((e: React.PointerEvent) => {
    if (disabled) return;
    if (!isDragging) return;
    updateFromEvent(e);
  }, [disabled, isDragging, updateFromEvent]);

  const onPointerUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  return (
    <div
      ref={containerRef}
      className={
        `relative w-64 h-64 select-none ` +
        (disabled ? 'opacity-70' : 'cursor-grab active:cursor-grabbing')
      }
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={onPointerUp}
      role="slider"
      aria-label="Vastu compass orientation"
      aria-valuemin={0}
      aria-valuemax={360}
      aria-valuenow={Math.round(angle)}
      tabIndex={0}
      onKeyDown={(e) => {
        if (disabled) return;
        const step = e.shiftKey ? 15 : 5;
        if (e.key === 'ArrowLeft') onChange(normalizeAngle(angle - step));
        if (e.key === 'ArrowRight') onChange(normalizeAngle(angle + step));
      }}
    >
      <div className="absolute inset-0 rounded-full bg-[#1F1F1F] shadow-lg" />
      <div className="absolute inset-2 rounded-full border border-white/10" />

      <svg className="absolute inset-0" viewBox="0 0 100 100" aria-hidden="true">
        <circle cx="50" cy="50" r="46" fill="none" stroke="rgba(198,167,94,0.35)" strokeWidth="1" />
        {Array.from({ length: 24 }).map((_, i) => {
          const a = (i * 360) / 24;
          const r1 = i % 6 === 0 ? 40 : 42;
          const r2 = 46;
          const rad = (a * Math.PI) / 180;
          const x1 = 50 + r1 * Math.cos(rad);
          const y1 = 50 + r1 * Math.sin(rad);
          const x2 = 50 + r2 * Math.cos(rad);
          const y2 = 50 + r2 * Math.sin(rad);
          return (
            <line
              key={i}
              x1={x1}
              y1={y1}
              x2={x2}
              y2={y2}
              stroke={i % 6 === 0 ? 'rgba(255,255,255,0.55)' : 'rgba(255,255,255,0.25)'}
              strokeWidth={i % 6 === 0 ? 1.2 : 0.7}
            />
          );
        })}

        <text x="50" y="14" textAnchor="middle" fill="white" fontSize="8" fontFamily="ui-sans-serif, system-ui">N</text>
        <text x="86" y="52" textAnchor="middle" fill="white" fontSize="8" fontFamily="ui-sans-serif, system-ui">E</text>
        <text x="50" y="91" textAnchor="middle" fill="white" fontSize="8" fontFamily="ui-sans-serif, system-ui">S</text>
        <text x="14" y="52" textAnchor="middle" fill="white" fontSize="8" fontFamily="ui-sans-serif, system-ui">W</text>
      </svg>

      <div className="absolute inset-0 flex items-center justify-center">
        <div className="w-2 h-2 rounded-full bg-[#C6A75E] shadow" />
      </div>

      <div className="absolute inset-0 flex items-center justify-center">
        <div
          className="w-full h-full"
          style={style}
          aria-hidden="true"
        >
          <div className="absolute left-1/2 top-[14px] -translate-x-1/2 w-[3px] h-[86px] rounded-full bg-[#C6A75E] shadow" />
          <div className="absolute left-1/2 top-[8px] -translate-x-1/2 w-0 h-0 border-l-[9px] border-r-[9px] border-b-[14px] border-l-transparent border-r-transparent border-b-[#C6A75E]" />
        </div>
      </div>

      <div className="absolute bottom-3 left-1/2 -translate-x-1/2 text-xs text-white/70">
        {Math.round(angle)}°
      </div>
    </div>
  );
});
