import React from 'react';
import { render, screen } from '@testing-library/react';
import HomePage from '.';

describe('HomePage', () => {
  test('renders the header', () => {
    render(<HomePage />);
    const headerElement = screen.getByRole('banner');
    expect(headerElement).toBeInTheDocument();
  });

  test('renders the React link', () => {
    render(<HomePage />);
    const linkElement = screen.getByText(/React/i);
    expect(linkElement).toBeInTheDocument();
  });
});
