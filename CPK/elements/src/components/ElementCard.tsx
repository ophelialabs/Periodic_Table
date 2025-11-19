'use client';

import React from 'react';
import { Element } from '@/lib/periodicTableData';

interface ElementCardProps {
  element: Element;
  onClose?: () => void;
}

export const ElementCard: React.FC<ElementCardProps> = ({ element, onClose }) => {
  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg p-6 text-white shadow-2xl max-w-md">
      <div className="flex justify-between items-start mb-4">
        <div>
          <div className="text-5xl font-bold">{element.symbol}</div>
          <div className="text-xl font-semibold text-gray-300">{element.name}</div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        )}
      </div>

      <div
        className="h-24 rounded mb-4 flex items-center justify-center text-white font-bold text-xl"
        style={{ backgroundColor: element.categoryColor }}
      >
        {element.category}
      </div>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-400">Atomic Number:</span>
          <span className="font-semibold">{element.atomicNumber}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Atomic Mass:</span>
          <span className="font-semibold">{element.atomicMass.toFixed(3)} u</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Period:</span>
          <span className="font-semibold">{element.period}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Group:</span>
          <span className="font-semibold">{element.group}</span>
        </div>
        {element.state && (
          <div className="flex justify-between">
            <span className="text-gray-400">State:</span>
            <span className="font-semibold">{element.state}</span>
          </div>
        )}
      </div>

      {(element.electronegativity ||
        element.ionizationEnergy ||
        element.density ||
        element.atomicRadius) && (
        <>
          <hr className="border-gray-700 my-4" />
          <div className="text-xs space-y-2">
            {element.electronegativity !== undefined && (
              <div className="flex justify-between">
                <span className="text-gray-400">Electronegativity:</span>
                <span className="font-semibold">{element.electronegativity.toFixed(2)}</span>
              </div>
            )}
            {element.ionizationEnergy !== undefined && (
              <div className="flex justify-between">
                <span className="text-gray-400">Ionization Energy:</span>
                <span className="font-semibold">{element.ionizationEnergy.toFixed(2)} eV</span>
              </div>
            )}
            {element.atomicRadius !== undefined && (
              <div className="flex justify-between">
                <span className="text-gray-400">Atomic Radius:</span>
                <span className="font-semibold">{element.atomicRadius} pm</span>
              </div>
            )}
            {element.density !== undefined && (
              <div className="flex justify-between">
                <span className="text-gray-400">Density:</span>
                <span className="font-semibold">{element.density.toFixed(3)} g/cm³</span>
              </div>
            )}
          </div>
        </>
      )}

      {(element.meltingPoint || element.boilingPoint) && (
        <>
          <hr className="border-gray-700 my-4" />
          <div className="text-xs space-y-2">
            {element.meltingPoint !== undefined && (
              <div className="flex justify-between">
                <span className="text-gray-400">Melting Point:</span>
                <span className="font-semibold">{element.meltingPoint}°C</span>
              </div>
            )}
            {element.boilingPoint !== undefined && (
              <div className="flex justify-between">
                <span className="text-gray-400">Boiling Point:</span>
                <span className="font-semibold">{element.boilingPoint}°C</span>
              </div>
            )}
          </div>
        </>
      )}

      {element.yearDiscovered && element.yearDiscovered > 0 && (
        <>
          <hr className="border-gray-700 my-4" />
          <div className="text-xs flex justify-between">
            <span className="text-gray-400">Year Discovered:</span>
            <span className="font-semibold">{element.yearDiscovered}</span>
          </div>
        </>
      )}
    </div>
  );
};
