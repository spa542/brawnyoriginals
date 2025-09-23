import React, { useState } from 'react';
import { FaYoutube, FaTiktok } from 'react-icons/fa';

const ContactPage: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission here
    console.log('Form submitted:', formData);
    alert('Thank you for your message! I will get back to you soon.');
    setFormData({ name: '', email: '', message: '' });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
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
                value={formData.message}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-2 border-gray-300 shadow-sm focus:border-tertiary-600 focus:ring-2 focus:ring-tertiary-500/50 text-primary transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-tertiary-500/30"
                required
              />
            </div>
            <div>
              <button
                type="submit"
                className="w-full md:w-auto bg-tertiary-600 text-white px-8 py-3 rounded-md border border-primary hover:bg-tertiary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-tertiary-500 transition-colors duration-300 font-medium"
              >
                Send Message
              </button>
            </div>
          </form>

          {/* Social Media & Content Links */}
          <div className="mt-12">
            <div className="flex flex-col md:flex-row items-center justify-center gap-8 md:gap-16">
              {/* Social Media Section */}
              <div className="text-center">
                <h3 className="text-lg font-medium text-primary mb-3">Follow Us on Social Media</h3>
                <div className="flex justify-center space-x-6">
                  <a 
                    href="https://www.youtube.com/@brawnyoriginals" 
                    target="_blank" 
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
                  <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                  </svg>
                </a>
              </div>
            </div>
          
          </div>
        </div>

        {/* Latest Content Header */}
        <div id="latest-content" className="text-center py-8">
          <h2 className="text-3xl font-bold text-primary mb-3">Check Out Our Latest Content</h2>
          <p className="text-primary text-opacity-90 max-w-2xl mx-auto">
            Stay updated with our newest videos, shorts, and fitness tips.
          </p>
        </div>

        {/* YouTube Video Section */}
        <div className="bg-secondary p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold text-primary mb-6">Latest YouTube Video</h2>
          <div className="aspect-w-16 aspect-h-9 bg-gray-100 rounded-lg overflow-hidden mb-4">
            <div className="w-full h-full flex items-center justify-center text-gray-400">
              [YouTube Video Embed]
            </div>
          </div>
        </div>

        {/* Shorts Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* YouTube Short */}
          <div className="bg-secondary p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-bold text-primary mb-4">Latest Short</h3>
            <div className="aspect-[9/16] bg-gray-100 rounded-lg overflow-hidden mb-4">
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                [YouTube Short/Reel]
              </div>
            </div>
          </div>

          {/* TikTok */}
          <div className="bg-secondary p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-bold text-primary mb-4">Latest TikTok</h3>
            <div className="aspect-[9/16] bg-gray-100 rounded-lg overflow-hidden mb-4">
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                [TikTok Embed]
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;
