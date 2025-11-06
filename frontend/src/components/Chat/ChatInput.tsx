/**
 * Chat Input Component
 * ====================
 * Text input area with send button and file upload
 * 
 * For beginners: This is the text box where users type messages!
 */

import React, { useState, KeyboardEvent } from 'react';
import { Send, Paperclip, Loader2 } from 'lucide-react';
import { Button } from '../ui/Button';
import { cn } from '@/lib/utils';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  onFileUpload: (file: File) => void;
  disabled?: boolean;
  isLoading?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  onFileUpload,
  disabled = false,
  isLoading = false,
}) => {
  const [message, setMessage] = useState('');

  // Handle sending message
  const handleSend = () => {
    if (message.trim() && !disabled && !isLoading) {
      onSendMessage(message);
      setMessage(''); // Clear input after sending
    }
  };

  // Handle Enter key press (send message)
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onFileUpload(file);
      e.target.value = ''; // Reset input
    }
  };

  return (
    <div className="border-t bg-background p-4">
      <div className="mx-auto max-w-4xl">
        <div className="flex items-end gap-2">
          {/* File Upload Button */}
          <label htmlFor="file-upload">
            <Button
              type="button"
              variant="outline"
              size="icon"
              disabled={disabled || isLoading}
              className="shrink-0"
              onClick={() => document.getElementById('file-upload')?.click()}
            >
              <Paperclip className="h-4 w-4" />
            </Button>
            <input
              id="file-upload"
              type="file"
              accept=".pdf,.docx,.doc,.txt"
              onChange={handleFileChange}
              className="hidden"
            />
          </label>

          {/* Message Input */}
          <div className="relative flex-1">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me anything about your documents..."
              disabled={disabled || isLoading}
              className={cn(
                'w-full resize-none rounded-md border border-input bg-background px-4 py-3 pr-12 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
                'min-h-[52px] max-h-[200px]'
              )}
              rows={1}
              style={{
                height: 'auto',
                minHeight: '52px',
              }}
              onInput={(e) => {
                const target = e.target as HTMLTextAreaElement;
                target.style.height = 'auto';
                target.style.height = `${target.scrollHeight}px`;
              }}
            />

            {/* Send Button (inside textarea) */}
            <Button
              type="button"
              size="icon"
              onClick={handleSend}
              disabled={!message.trim() || disabled || isLoading}
              className="absolute bottom-2 right-2 h-8 w-8"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
        </div>

        {/* Helper Text */}
        <p className="mt-2 text-xs text-muted-foreground">
          Press <kbd className="rounded bg-muted px-1">Enter</kbd> to send,{' '}
          <kbd className="rounded bg-muted px-1">Shift + Enter</kbd> for new line
        </p>
      </div>
    </div>
  );
};
