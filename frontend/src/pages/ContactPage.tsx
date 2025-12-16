import React, { useState, useCallback } from 'react';
import { FaYoutube, FaTiktok, FaInstagram } from 'react-icons/fa';
import YouTubeEmbed from '../components/YouTubeEmbed';
import TikTokEmbed from '../components/TikTokEmbed';
import VideoLoader from '../components/VideoLoader';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import ReCAPTCHA from '../components/ReCAPTCHA';
import { getBaseUrl } from '../utils/helpers';

const ContactPage: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [recaptchaToken, setRecaptchaToken] = useState('');
  const [recaptchaReady, setRecaptchaReady] = useState(false);
  const [formSubmitted, setFormSubmitted] = useState(false);


  const handleRecaptchaVerify = useCallback((token: string) => {
    setRecaptchaToken(token);
    setRecaptchaReady(true);
    
    // If form was already submitted but waiting for reCAPTCHA, submit now
    if (formSubmitted) {
      handleFormSubmission();
    }
  }, [formSubmitted]);

  const handleFormSubmission = async () => {
    if (!recaptchaReady) {
      setFormSubmitted(true);
      return;
    }

    setIsSubmitting(true);
    
    try {
      const baseUrl = getBaseUrl(); 
      const response = await fetch(`${baseUrl}/api/contact/email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          g_recaptcha_response: recaptchaToken
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      await response.json();
      
      // Show success message
      toast.success(
        'Message sent successfully! \nWe\'ll get back to you soon.',
        {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: false,
          draggable: true,
          progress: undefined,
        }
      );
      
      // Reset form and reCAPTCHA
      setFormData({ name: '', email: '', message: '' });
      setRecaptchaToken('');
      setRecaptchaReady(false);
      setFormSubmitted(false);
    } catch (error) {
      console.error('Error submitting form:', error);
      toast.error(
        'Sorry, we couldn\'t send your message. \nPlease try again later.',
        {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: false,
          draggable: true,
          progress: undefined,
        }
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleFormSubmission();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <ToastContainer
        position="top-center"
        autoClose={5000}
        toastStyle={{ whiteSpace: 'pre-line' }}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-primary mb-4">Get In Touch</h1>
        <p className="text-xl text-primary text-opacity-90 max-w-3xl mx-auto">
          Have questions about our programs or want to learn more? Reach out to us and we'll get back to you as soon as possible.
        </p>
      </div>

      <div className="space-y-12">
        {/* Contact Form Section */}
        <div className="bg-secondary p-8 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold text-primary mb-6">Send Us a Message</h2>
          <p className="text-primary text-opacity-90 mb-8">
            Have questions or want to learn more about our programs? Send us a message and we'll get back to you soon.
          </p>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-primary mb-1">Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-2 border-gray-300 shadow-sm focus:border-tertiary-600 focus:ring-2 focus:ring-tertiary-500/50 text-primary transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-tertiary-500/30"
                  required
                />
              </div>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-primary mb-1">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-2 border-gray-300 shadow-sm focus:border-tertiary-600 focus:ring-2 focus:ring-tertiary-500/50 text-primary transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-tertiary-500/30"
                  required
                />
              </div>
            </div>
            <div>
              <label htmlFor="message" className="block text-sm font-medium text-primary mb-1">Message</label>
              <textarea
                id="message"
                name="message"
                rows={4}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-2 border-gray-300 shadow-sm focus:border-tertiary-600 focus:ring-2 focus:ring-tertiary-500/50 text-primary transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-tertiary-500/30"
                required
              />
            </div>
            <div className="space-y-4">
              <div className="text-xs text-gray-500">
                This site is protected by reCAPTCHA and the Google
                <a href="https://policies.google.com/privacy" className="text-tertiary-600 hover:underline ml-1">Privacy Policy</a> and
                <a href="https://policies.google.com/terms" className="text-tertiary-600 hover:underline ml-1">Terms of Service</a> apply.
              </div>
              <button
                type="submit"
                disabled={isSubmitting || !recaptchaReady}
                className={`w-full md:w-auto bg-tertiary-600 text-white px-8 py-3 rounded-md border border-primary hover:bg-tertiary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-tertiary-500 transition-colors duration-300 font-medium ${
                  isSubmitting ? 'opacity-70 cursor-not-allowed' : !recaptchaReady ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                {isSubmitting ? 'Sending...' : 'Send Message'}
              </button>
              <ReCAPTCHA 
                sitekey="6Ldh-dorAAAAAG7kBeNcDUsLM5PtgfZPip2f9jwH" 
                action="contact_form_submit"
                onVerify={handleRecaptchaVerify}
              />
            </div>
          </form>

          {/* Social Media & Content Links */}
          <div className="mt-12">
            <div className="flex flex-col md:flex-row items-center justify-center gap-8 md:gap-16">
              <div className="text-center">
                <h3 className="text-lg font-medium text-primary mb-3">Follow Us on Social Media</h3>
                <div className="flex justify-center space-x-6">
                  <a 
                    href="https://www.youtube.com/@brawnyoriginals" 
                    rel="noopener noreferrer"
                    className="text-primary hover:text-tertiary-600 transition-colors" 
                    aria-label="YouTube"
                  >
                    <FaYoutube size={24} />
                  </a>
                  <a 
                    href="https://www.tiktok.com/@brawny_originals" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-primary hover:text-tertiary-600 transition-colors" 
                    aria-label="TikTok"
                  >
                    <FaTiktok size={24} />
                  </a>
                  <a 
                    href="https://www.instagram.com/brawny_originals/" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-primary hover:text-tertiary-600 transition-colors" 
                    aria-label="Instagram"
                  >
                    <FaInstagram size={24} />
                  </a>
                </div>
              </div>
              
              {/* Vertical Divider - Hidden on mobile */}
              <div className="hidden md:block h-12 w-px bg-gray-300"></div>
              
              {/* Explore Content Section */}
              <div className="text-center">
                <h3 className="text-lg font-medium text-primary mb-3">Explore Our Content</h3>
                <a 
                  href="#latest-content" 
                  className="inline-flex items-center text-tertiary-600 hover:text-tertiary-800 transition-colors font-medium"
                  onClick={(e) => {
                    e.preventDefault();
                    document.getElementById('latest-content')?.scrollIntoView({ behavior: 'smooth' });
                  }}
                >
                  View Latest Videos & Shorts
                  <svg className="w-5 h-5 ml-2 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                  </svg>
                </a>
              </div>
            </div>
          
          </div>
        </div>

        {/* Latest Content Header */}
        <div id="latest-content" className="text-center pt-4 pb-2">
          <h2 className="text-3xl font-bold text-primary mb-2">Check Out Our Latest Content</h2>
          <p className="text-primary text-opacity-90 max-w-2xl mx-auto mb-4">
            Stay updated with our newest videos, shorts, and fitness tips.
          </p>
        </div>

        {/* YouTube Video Section */}
        <div className="bg-secondary p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold text-primary mb-6">Latest YouTube Video</h2>
          <VideoLoader type="youtube">
            {({ videoId }) => (
              <YouTubeEmbed 
                videoId={videoId}
                title="Latest YouTube video"
                className="mb-6"
              />
            )}
          </VideoLoader>
          <div className="text-center mt-8 mb-6">
            <button
              onClick={() => {
                const element = document.getElementById('shorts-section');
                if (element) {
                  const yOffset = -40; // Adjust this value to change how much above the element to scroll
                  const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
                  window.scrollTo({ top: y, behavior: 'smooth' });
                }
              }}
              className="inline-flex items-center text-tertiary-600 hover:text-tertiary-800 transition-colors font-medium"
            >
              View More Content
              <svg className="w-5 h-5 ml-2 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            </button>
          </div>
        </div>

        {/* Shorts Section */}
        <div id="shorts-section" className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
          {/* YouTube Short */}
          <div className="bg-secondary p-6 rounded-lg shadow-lg max-w-[400px] mx-auto w-full">
            <h3 className="text-xl font-bold text-primary mb-4">Latest Short</h3>
            <VideoLoader type="short">
              {({ videoId }) => (
                <YouTubeEmbed 
                  videoId={videoId}
                  title="Latest YouTube Short"
                  isShort={true}
                />
              )}
            </VideoLoader>
          </div>

          {/* TikTok */}
          <div className="bg-secondary p-6 rounded-lg shadow-lg max-w-[400px] mx-auto w-full">
            <h3 className="text-xl font-bold text-primary mb-4">Latest TikTok</h3>
            <VideoLoader type="tiktok">
              {({ videoId }) => (
                <TikTokEmbed 
                  videoId={videoId}
                  title="Latest TikTok Video"
                />
              )}
            </VideoLoader>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;
