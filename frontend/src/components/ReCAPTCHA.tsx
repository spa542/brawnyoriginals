import { useEffect, useRef, useState } from 'react';

declare global {
  interface Window {
    grecaptcha?: {
      ready: (callback: () => void) => void;
      execute: (sitekey: string, options: { action: string }) => Promise<string>;
    };
  }
}

interface ReCAPTCHAProps {
  onVerify: (token: string) => void;
  action: string;
  sitekey: string;
  maxRetries?: number;
  retryDelay?: number;
}

export const ReCAPTCHA = ({
  onVerify,
  action,
  sitekey,
  maxRetries = 3,
  retryDelay = 1000,
}: ReCAPTCHAProps) => {
  const recaptchaRef = useRef<HTMLDivElement>(null);
  const badgeRef = useRef<HTMLDivElement>(null);
  const [isScriptLoaded, setIsScriptLoaded] = useState(false);
  const retryCount = useRef(0);
  const scriptId = 'google-recaptcha-v3';

  const executeRecaptcha = async () => {
    if (!window.grecaptcha) {
      console.error('reCAPTCHA not loaded');
      onVerify('');
      return;
    }

    try {
      const token = await window.grecaptcha.execute(sitekey, { action });
      onVerify(token);
    } catch (error) {
      console.error('reCAPTCHA execution error:', error);
      onVerify('');
    }
  };

  const loadRecaptcha = () => {
    // Check if script is already loaded
    if (document.getElementById(scriptId) || window.grecaptcha) {
      setIsScriptLoaded(true);
      return;
    }

    const script = document.createElement('script');
    script.id = scriptId;
    script.src = `https://www.recaptcha.net/recaptcha/api.js?render=${sitekey}`;
    script.async = true;
    script.defer = true;

    script.onload = () => {
      setIsScriptLoaded(true);
      retryCount.current = 0;
    };

    script.onerror = () => {
      console.error('Failed to load reCAPTCHA script');
      if (retryCount.current < maxRetries) {
        retryCount.current += 1;
        console.log(`Retrying reCAPTCHA load (${retryCount.current}/${maxRetries})...`);
        setTimeout(loadRecaptcha, retryDelay * retryCount.current);
      } else {
        console.error('Max retries reached for reCAPTCHA load');
        onVerify('');
      }
    };

    document.head.appendChild(script);
  };

  useEffect(() => {
    loadRecaptcha();

    return () => {
      const script = document.getElementById(scriptId);
      if (script) {
        document.head.removeChild(script);
      }
    };
  }, [sitekey]);

  useEffect(() => {
    if (isScriptLoaded) {
      window.grecaptcha?.ready(executeRecaptcha);
    }
  }, [action, isScriptLoaded]);

  return (
    <div>
      <div ref={recaptchaRef} />
      <div ref={badgeRef} className="grecaptcha-badge" />
    </div>
  );
};

export default ReCAPTCHA;
