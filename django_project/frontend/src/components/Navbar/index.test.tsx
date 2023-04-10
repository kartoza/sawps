import React from 'react';
import { render, screen } from '@testing-library/react';
import ResponsiveNavbar from '.';

describe('HomePage', () => {
  test('renders the header', () => {
    render(<ResponsiveNavbar />);
    const headerElement = screen.getByRole('banner');
    expect(headerElement).toBeInTheDocument();
  });

  test('renders the menu', () => {
    render(<ResponsiveNavbar />);
    const linkElement = screen.getAllByText(/Map/i);
    expect(linkElement).not.toBeNull();
  });
});