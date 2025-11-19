'use client';

import React, { useEffect, useRef } from 'react';
import { Element, PERIODIC_TABLE } from '@/lib/periodicTableData';

interface DataVisualizationProps {
  type: 'scatter' | 'histogram' | 'heatmap';
  selectedElements?: Element[];
  property?: 'atomicMass' | 'electronegativity' | 'ionizationEnergy' | 'density';
}

export const DataVisualization: React.FC<DataVisualizationProps> = ({
  type,
  selectedElements = PERIODIC_TABLE,
  property = 'atomicMass',
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const plotlyScript = document.createElement('script');
    plotlyScript.src = 'https://cdn.plot.ly/plotly-latest.min.js';
    plotlyScript.async = true;
    plotlyScript.onload = () => {
      renderVisualization();
    };
    document.body.appendChild(plotlyScript);

    const renderVisualization = () => {
      const Plotly = (window as any).Plotly;
      if (!Plotly) return;

      const data = selectedElements.map(el => ({
        symbol: el.symbol,
        name: el.name,
        value: el[property as keyof Element] as number,
        category: el.category,
      })).filter(d => d.value !== undefined && typeof d.value === 'number');

      if (type === 'scatter') {
        const trace = {
          x: data.map(d => d.symbol),
          y: data.map(d => d.value),
          mode: 'markers',
          type: 'scatter',
          marker: {
            size: 10,
            color: data.map(d => hashCode(d.category) % 360),
            colorscale: 'Viridis',
            showscale: true,
          },
          text: data.map(d => `${d.name}<br>${property}: ${d.value.toFixed(2)}`),
          hoverinfo: 'text',
        };

        const layout = {
          title: `${property} Distribution`,
          xaxis: { title: 'Element' },
          yaxis: { title: property },
          hovermode: 'closest',
          plot_bgcolor: '#1a1a2e',
          paper_bgcolor: '#0f0f1e',
          font: { color: '#ffffff' },
        };

        Plotly.newPlot(containerRef.current, [trace], layout, { responsive: true });
      } else if (type === 'histogram') {
        const trace = {
          x: data.map(d => d.value),
          type: 'histogram',
          marker: { color: '#6366f1' },
          opacity: 0.7,
        };

        const layout = {
          title: `${property} Histogram`,
          xaxis: { title: property },
          yaxis: { title: 'Frequency' },
          plot_bgcolor: '#1a1a2e',
          paper_bgcolor: '#0f0f1e',
          font: { color: '#ffffff' },
        };

        Plotly.newPlot(containerRef.current, [trace], layout, { responsive: true });
      }
    };

    return () => {
      if (plotlyScript.parentNode) {
        document.body.removeChild(plotlyScript);
      }
    };
  }, [type, selectedElements, property]);

  return (
    <div
      ref={containerRef}
      style={{
        width: '100%',
        height: '100%',
        minHeight: '400px',
      }}
    />
  );
};

function hashCode(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash;
  }
  return Math.abs(hash);
}
