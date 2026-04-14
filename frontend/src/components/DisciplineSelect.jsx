import React, { useMemo } from "react";

/**
 * DisciplineSelect — 3-level dependent: Discipline → Trade → Skill
 *
 * Props:
 *   grouped   [{id, name, trades:[{id, name, skills:[]}]}]  — from /trades API
 *   value     { discipline: "", trade: "", skill: "" }
 *   onChange  (val) => void
 *   required  bool
 */
export default function DisciplineSelect({
  grouped = [],
  value = {},
  onChange,
  required = false,
  "data-testid": testId,
  className = "",
}) {
  const { discipline = "", trade = "", skill = "" } = value;

  // Memoize each filtered list to avoid unnecessary re-renders
  const disciplineList = useMemo(() => grouped, [grouped]);

  const tradeList = useMemo(() => {
    const disc = grouped.find((g) => g.name === discipline);
    return disc ? disc.trades || [] : [];
  }, [grouped, discipline]);

  const skillList = useMemo(() => {
    const tradeObj = tradeList.find((t) => t.name === trade);
    return tradeObj ? tradeObj.skills || [] : [];
  }, [tradeList, trade]);

  const handleDiscipline = (v) => onChange({ discipline: v, trade: "", skill: "" });
  const handleTrade = (v) => onChange({ discipline, trade: v, skill: "" });
  const handleSkill = (v) => onChange({ discipline, trade, skill: v });

  const base =
    `w-full border border-slate-300 dark:border-slate-600 rounded-lg px-3 py-2.5 text-sm ` +
    `focus:outline-none focus:border-[#0000FF] dark:bg-slate-800 dark:text-white bg-white ${className}`;

  return (
    <div className="space-y-2" data-testid={testId}>
      {/* Level 1: Discipline */}
      <select
        value={discipline}
        onChange={(e) => handleDiscipline(e.target.value)}
        required={required}
        className={base}
        data-testid={testId ? `${testId}-discipline` : undefined}
      >
        <option value="">Select Discipline</option>
        {disciplineList.map((d) => (
          <option key={d.id || d.name} value={d.name}>{d.name}</option>
        ))}
      </select>

      {/* Level 2: Trade — enabled only when discipline selected */}
      <select
        value={trade}
        onChange={(e) => handleTrade(e.target.value)}
        disabled={!discipline}
        required={required && !!discipline}
        className={base + (!discipline ? " opacity-50 cursor-not-allowed" : "")}
        data-testid={testId ? `${testId}-trade` : undefined}
      >
        <option value="">{discipline ? "Select Trade" : "— select discipline first —"}</option>
        {tradeList.map((t) => (
          <option key={t.id || t.name} value={t.name}>{t.name}</option>
        ))}
      </select>

      {/* Level 3: Skill — optional, enabled only when trade selected */}
      <select
        value={skill}
        onChange={(e) => handleSkill(e.target.value)}
        disabled={!trade}
        className={base + (!trade ? " opacity-50 cursor-not-allowed" : "")}
        data-testid={testId ? `${testId}-skill` : undefined}
      >
        <option value="">{trade ? "Select Skill (optional)" : "— select trade first —"}</option>
        {skillList.map((s) => (
          <option key={s} value={s}>{s}</option>
        ))}
      </select>
    </div>
  );
}
