export function gradeColor(value: number) {
  if (value >= 80) return "success";
  if (value >= 60) return "warning";
  return "error";
}
