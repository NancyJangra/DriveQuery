/**
 * Chat Message Component
 * ======================
 * Displays a single chat message (user or AI)
 * 
 * For beginners: This is just a styled div that shows messages!
 */

import React from 'react';
import { Bot, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  sources?: string[];
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  role,
  content,
  timestamp,
  sources,
}) => {
  const isUser = role === 'user';

  return (
    <div
      className={cn(
        'flex gap-3 p-4 message-appear',
        isUser ? 'bg-muted/50' : 'bg-background'
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full',
          isUser ? 'bg-primary' : 'bg-secondary'
        )}
      >
        {isUser ? (
          <User className="h-4 w-4 text-primary-foreground" />
        ) : (
          <Bot className="h-4 w-4 text-secondary-foreground" />
        )}
      </div>

      {/* Message Content */}
      <div className="flex-1 space-y-2">
        {/* Role Label */}
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold">
            {isUser ? 'You' : 'AutoQuery AI'}
          </span>
          {timestamp && (
            <span className="text-xs text-muted-foreground">{timestamp}</span>
          )}
        </div>

        {/* Message Text */}
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>

        {/* Sources (if any) */}
        {sources && sources.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            <span className="text-xs text-muted-foreground">Sources:</span>
            {sources.map((source, index) => (
              <span
                key={index}
                className="rounded-full bg-primary/10 px-2 py-1 text-xs text-primary"
              >
                📄 {source}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
