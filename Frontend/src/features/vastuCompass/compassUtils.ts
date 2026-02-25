export type Cardinal = 'north' | 'east' | 'south' | 'west';

export function normalizeAngle(angle: number): number {
  const a = angle % 360;
  return a < 0 ? a + 360 : a;
}

export function snapAngle(angle: number, stepDegrees = 90): number {
  const a = normalizeAngle(angle);
  const snapped = Math.round(a / stepDegrees) * stepDegrees;
  return normalizeAngle(snapped);
}

export function angleToMappedDirections(angle: number): Record<Cardinal, Cardinal> {
  const a = normalizeAngle(angle);
  const steps = Math.round(a / 90) % 4;

  const base: Cardinal[] = ['north', 'east', 'south', 'west'];
  const rotateRight = (arr: Cardinal[], k: number) => {
    const n = arr.length;
    const r = ((k % n) + n) % n;
    return [...arr.slice(n - r), ...arr.slice(0, n - r)];
  };

  const labelsForSlots = rotateRight(base, steps);

  return {
    north: labelsForSlots[0],
    east: labelsForSlots[1],
    south: labelsForSlots[2],
    west: labelsForSlots[3],
  };
}
