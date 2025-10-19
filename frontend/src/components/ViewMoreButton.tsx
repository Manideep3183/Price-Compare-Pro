import React from 'react';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface ViewMoreButtonProps {
  expanded: boolean;
  onClick: () => void;
  totalItems: number;
  currentlyShowing: number;
}

export const ViewMoreButton = ({
  expanded,
  onClick,
  totalItems,
  currentlyShowing,
}: ViewMoreButtonProps) => {
  return (
    <div className="flex justify-center animate-fade-in">
      <Button
        onClick={onClick}
        variant="outline"
        size="lg"
        className="w-full max-w-md mt-6 bg-gradient-to-r from-primary/10 to-accent/10 hover:from-primary/20 hover:to-accent/20 transition-all duration-300 border-2 border-primary/30 hover:border-primary hover:scale-105 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl font-semibold text-base"
      >
        {expanded ? (
          <>
            <ChevronUp className="h-5 w-5 animate-bounce" />
            <span>Show Less</span>
          </>
        ) : (
          <>
            <ChevronDown className="h-5 w-5 animate-bounce" />
            <span>
              View {totalItems - currentlyShowing} More Products
            </span>
          </>
        )}
      </Button>
    </div>
  );
};