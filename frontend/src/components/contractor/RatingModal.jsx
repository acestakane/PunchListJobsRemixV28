import React, { useState } from "react";
import { X, Loader2 } from "lucide-react";

/**
 * RatingModal — contractor rates crew members after job completion.
 * Props:
 *   job          — job object (must have .crew_accepted, .id)
 *   onClose      — close without submitting
 *   onSubmit     — fn(job, ratings, reviews, skipped) called on Submit
 *   crewNames    — { [crewId]: name } map for display (optional, falls back to ID)
 *   isSubmitting — boolean indicating submission in progress
 */
export function RatingModal({ job, onClose, onSubmit, crewNames = {}, isSubmitting = false }) {
  const [ratings, setRatings] = useState({});
  const [reviews, setReviews] = useState({});
  const [skipped, setSkipped] = useState(new Set());
  const [validationError, setValidationError] = useState("");

  if (!job?.crew_accepted?.length) return null;

  const toggleSkip = (crewId) => {
    setValidationError(""); // Clear error on interaction
    setSkipped(prev => {
      const next = new Set(prev);
      if (next.has(crewId)) next.delete(crewId);
      else {
        next.add(crewId);
        // Clear star selection when skipping
        setRatings(r => { const n = { ...r }; delete n[crewId]; return n; });
      }
      return next;
    });
  };

  const setRating = (crewId, stars) => {
    setValidationError(""); // Clear error on interaction
    setRatings(r => ({ ...r, [crewId]: stars }));
    // Auto-unskip if they're selecting stars
    if (skipped.has(crewId)) {
      setSkipped(prev => {
        const next = new Set(prev);
        next.delete(crewId);
        return next;
      });
    }
  };

  const handleSubmit = () => {
    // Validate at least one crew member is handled
    const hasAnyAction = job.crew_accepted.some(crewId => 
      (ratings[crewId] && ratings[crewId] > 0) || skipped.has(crewId)
    );

    if (!hasAnyAction) {
      setValidationError("Please rate or skip at least one crew member before submitting");
      return;
    }

    setValidationError("");
    onSubmit(job, ratings, reviews, skipped);
  };

  const getName = (id) => crewNames[id] || `Worker ${id.slice(0, 6)}`;

  // Count handled crew members for progress indicator
  const handledCount = job.crew_accepted.filter(crewId => 
    (ratings[crewId] && ratings[crewId] > 0) || skipped.has(crewId)
  ).length;

  return (
    <div className="fixed inset-0 bg-black/50 z-[10] flex items-center justify-center p-4">
      <div className="card max-w-md w-full p-6 relative max-h-[90vh] overflow-y-auto">
        <button 
          onClick={onClose} 
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 disabled:opacity-50"
          disabled={isSubmitting}
          aria-label="Close"
        >
          <X className="w-5 h-5" />
        </button>
        <h2 className="font-extrabold text-[#050A30] dark:text-white text-xl mb-2" style={{ fontFamily: "Manrope, sans-serif" }}>
          Rate Workers
        </h2>
        <p className="text-sm text-slate-500 mb-4">
          Progress: {handledCount} of {job.crew_accepted.length} handled
        </p>

        {validationError && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {validationError}
          </div>
        )}

        {job.crew_accepted.map(crewId => (
          <div key={crewId} className="mb-4 p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm font-semibold truncate max-w-[60%]">{getName(crewId)}</p>
              <button
                onClick={() => toggleSkip(crewId)}
                disabled={isSubmitting}
                className={`text-xs px-2 py-0.5 rounded font-bold transition-colors disabled:opacity-50 ${
                  skipped.has(crewId)
                    ? "bg-slate-300 dark:bg-slate-600 text-slate-700 dark:text-slate-200"
                    : "bg-slate-100 dark:bg-slate-700 text-slate-500 hover:bg-slate-200"
                }`}
                data-testid={`skip-crew-${crewId}`}
              >
                {skipped.has(crewId) ? "Skipped" : "Skip"}
              </button>
            </div>
            {!skipped.has(crewId) && (
              <>
                <div className="flex gap-1 mb-2">
                  {[1, 2, 3, 4, 5].map(s => (
                    <button 
                      key={s} 
                      onClick={() => setRating(crewId, s)}
                      disabled={isSubmitting}
                      className={`text-2xl transition-colors disabled:opacity-50 ${
                        (ratings[crewId] || 0) >= s ? "text-amber-400" : "text-slate-300"
                      }`}
                      aria-label={`Rate ${s} stars`}
                    >
                      ★
                    </button>
                  ))}
                </div>
                <textarea 
                  placeholder="Write a review (optional)…" 
                  value={reviews[crewId] || ""}
                  onChange={e => setReviews(r => ({ ...r, [crewId]: e.target.value }))}
                  disabled={isSubmitting}
                  className="w-full border border-slate-200 dark:border-slate-600 rounded-lg p-2 text-sm dark:bg-slate-700 dark:text-white disabled:opacity-50 disabled:cursor-not-allowed" 
                  rows={2} 
                />
              </>
            )}
          </div>
        ))}

        <button
          onClick={handleSubmit}
          disabled={isSubmitting || handledCount === 0}
          className="w-full bg-[#0000FF] text-white py-3 rounded-xl font-bold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          data-testid="submit-ratings-btn"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Submitting...
            </>
          ) : (
            "Submit Ratings"
          )}
        </button>
        
        {handledCount === 0 && (
          <p className="text-xs text-center text-slate-500 mt-2">
            Rate or skip at least one crew member to continue
          </p>
        )}
      </div>
    </div>
  );
}
