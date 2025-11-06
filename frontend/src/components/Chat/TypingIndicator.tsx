/**
 * Typing Indicator Component
 * ==========================
 * Shows animated dots when AI is thinking
 * 
 * For beginners: This makes it look like the AI is "typing"!
 */

import React from 'react';
import { Bot } from 'lucide-react';

export const TypingIndicator: React.FC = () => {
  return (
    <div className="flex gap-3 p-4 bg-background">
      {/* AI Avatar */}
      <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full bg-secondary">
        <Bot className="h-4 w-4 text-secondary-foreground" />
      </div>

      {/* Typing Animation */}
      <div className="flex items-center gap-1 pt-1">
        <div className="typing-dot h-2 w-2 rounded-full bg-muted-foreground" />
        <div className="typing-dot h-2 w-2 rounded-full bg-muted-foreground" />
        <div className="typing-dot h-2 w-2 rounded-full bg-muted-foreground" />
      </div>
    </div>
  );
};
