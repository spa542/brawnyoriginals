import { useEffect, useRef } from 'react';

declare global {
  interface Window {
    grecaptcha: any;
  }
}

interface ReCAPTCHAProps {
  onVerify: (token: string) => void;
  action: string;
  sitekey: string;
}

export const ReCAPTCHA = ({ onVerify, action, sitekey }: ReCAPTCHAProps) => {
  const recaptchaRef = useRef<HTMLDivElement>(null);
  const badgeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Load reCAPTCHA script
    const script = document.createElement('script');
    script.src = `https://www.google.com/recaptcha/api.js?render=${sitekey}`;
    script.async = true;
    script.defer = true;
    script.onload = () => {
      // Initialize reCAPTCHA
      window.grecaptcha.ready(() => {
        // Execute reCAPTCHA with the action
        window.grecaptcha.execute(sitekey, { action })
          .then((token: string) => {
            onVerify(token);
          })
          .catch((error: Error) => {
            console.error('reCAPTCHA error:', error);
            // Continue with form submission even if reCAPTCHA fails
            onVerify('');
          });
      });
    };
    
    document.head.appendChild(script);

    return () => {
      // Clean up
      document.head.removeChild(script);
    };
  }, [action, onVerify, sitekey]);

  return (
    <div>
      <div ref={recaptchaRef} />
      <div ref={badgeRef} className="grecaptcha-badge" />
    </div>
  );
};

export default ReCAPTCHA;
