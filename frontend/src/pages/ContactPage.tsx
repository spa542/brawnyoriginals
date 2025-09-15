import React, { useState } from 'react';
import { FaPhone, FaMapMarkerAlt, FaInstagram, FaYoutube, FaTiktok, FaFacebook } from 'react-icons/fa';

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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Contact Form */}
        <div className="bg-secondary p-8 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold text-primary mb-6">Send Us a Message</h2>
          <form onSubmit={handleSubmit} className="space-y-6">
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
                className="bg-tertiary-600 text-white px-8 py-3 rounded-md hover:bg-tertiary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-tertiary-500 transition-colors duration-300 font-medium"
              >
                Send Message
              </button>
            </div>
          </form>
        </div>

        {/* Contact Info & Socials */}
        <div className="space-y-8">
          {/* Contact Info */}
          <div className="bg-secondary p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-primary mb-6">Contact Information</h2>
            <div className="space-y-4">
              <div className="flex items-start">
                <FaPhone className="text-tertiary-600 mt-1 mr-3 flex-shrink-0" size={20} />
                <div>
                  <h3 className="font-medium text-primary">Phone</h3>
                  <a href="tel:+1234567890" className="text-primary text-opacity-80 hover:text-opacity-100 transition-colors">
                    (123) 456-7890
                  </a>
                </div>
              </div>
              <div className="flex items-start">
                <FaMapMarkerAlt className="text-tertiary-600 mt-1 mr-3 flex-shrink-0" size={20} />
                <div>
                  <h3 className="font-medium text-primary">Location</h3>
                  <p className="text-primary text-opacity-80">
                    [Your Business Address Here]
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Social Media */}
          <div className="bg-secondary p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-primary mb-6">Follow Us</h2>
            <div className="flex space-x-4">
              <a href="#" className="text-primary hover:text-tertiary-600 transition-colors" aria-label="Instagram">
                <FaInstagram size={24} />
              </a>
              <a href="#" className="text-primary hover:text-tertiary-600 transition-colors" aria-label="YouTube">
                <FaYoutube size={24} />
              </a>
              <a href="#" className="text-primary hover:text-tertiary-600 transition-colors" aria-label="TikTok">
                <FaTiktok size={24} />
              </a>
              <a href="#" className="text-primary hover:text-tertiary-600 transition-colors" aria-label="Facebook">
                <FaFacebook size={24} />
              </a>
            </div>
          </div>

          {/* Additional Resources */}
          <div className="bg-secondary p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-primary mb-4">Additional Resources</h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-medium text-primary mb-2">YouTube Channel</h3>
                <p className="text-primary text-opacity-80 mb-2">Check out our latest training videos and tutorials.</p>
                <a href="#" className="text-tertiary-600 hover:underline">
                  [YouTube Channel Link]
                </a>
              </div>
              <div>
                <h3 className="font-medium text-primary mb-2">Training Programs</h3>
                <p className="text-primary text-opacity-80 mb-2">Explore our customized training programs.</p>
                <a href="/programs" className="text-tertiary-600 hover:underline">
                  View Programs →
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
};

export default ContactPage;
