'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { Element, PERIODIC_TABLE } from '@/lib/periodicTableData';

interface PeriodicTable3DProps {
  onElementClick?: (element: Element) => void;
  selectedElement?: Element | null;
}

export const PeriodicTable3D: React.FC<PeriodicTable3DProps> = ({ onElementClick, selectedElement }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const cubesRef = useRef<Map<number, THREE.Mesh>>(new Map());
  const [hoveredElement, setHoveredElement] = useState<Element | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    sceneRef.current = scene;

    // Camera setup
    const camera = new THREE.PerspectiveCamera(
      75,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      1000
    );
    camera.position.set(15, 10, 15);
    camera.lookAt(8, 3, 0);
    cameraRef.current = camera;

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    renderer.shadowMap.enabled = true;
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    scene.add(directionalLight);

    // Create periodic table grid
    const spacing = 1.5;
    const cubes = new Map<number, THREE.Mesh>();

    PERIODIC_TABLE.forEach((element) => {
      const x = (element.group - 1) * spacing;
      const y = (7 - element.period) * spacing;

      const geometry = new THREE.BoxGeometry(1.3, 1.3, 1.3);
      const color = new THREE.Color(element.categoryColor);
      const material = new THREE.MeshPhongMaterial({
        color: color,
        emissive: 0x000000,
        shininess: 100,
      });

      const cube = new THREE.Mesh(geometry, material);
      cube.position.set(x, y, 0);
      cube.castShadow = true;
      cube.receiveShadow = true;
      cube.userData = { element, originalColor: color.clone() };

      scene.add(cube);
      cubes.set(element.atomicNumber, cube);
    });

    cubesRef.current = cubes;

    // Raycaster for mouse interaction
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const onMouseMove = (event: MouseEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(scene.children);

      // Reset all cubes
      cubes.forEach((cube) => {
        const material = cube.material as THREE.MeshPhongMaterial;
        material.emissive.setHex(0x000000);
      });

      if (intersects.length > 0) {
        const intersected = intersects[0].object as THREE.Mesh;
        if (intersected.userData?.element) {
          const material = intersected.material as THREE.MeshPhongMaterial;
          material.emissive.setHex(0xffffff);
          material.emissive.multiplyScalar(0.5);
          setHoveredElement(intersected.userData.element);
        }
      } else {
        setHoveredElement(null);
      }
    };

    const onClick = (event: MouseEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(scene.children);

      if (intersects.length > 0) {
        const intersected = intersects[0].object as THREE.Mesh;
        if (intersected.userData?.element && onElementClick) {
          onElementClick(intersected.userData.element);
        }
      }
    };

    renderer.domElement.addEventListener('mousemove', onMouseMove);
    renderer.domElement.addEventListener('click', onClick);

    // Animation loop
    let frameId: number;
    const animate = () => {
      frameId = requestAnimationFrame(animate);

      // Rotate view slightly
      camera.position.applyAxisAngle(new THREE.Vector3(0, 1, 0), 0.0002);
      camera.lookAt(8, 3, 0);

      // Update selected element highlight
      if (selectedElement) {
        const selectedCube = cubes.get(selectedElement.atomicNumber);
        if (selectedCube) {
          const material = selectedCube.material as THREE.MeshPhongMaterial;
          material.emissive.setHex(0xff6b6b);
          material.emissive.multiplyScalar(0.7);
        }
      }

      renderer.render(scene, camera);
    };

    animate();

    // Handle resize
    const handleResize = () => {
      if (!containerRef.current) return;
      const width = containerRef.current.clientWidth;
      const height = containerRef.current.clientHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      renderer.domElement.removeEventListener('mousemove', onMouseMove);
      renderer.domElement.removeEventListener('click', onClick);
      cancelAnimationFrame(frameId);
      containerRef.current?.removeChild(renderer.domElement);
    };
  }, [onElementClick, selectedElement]);

  return (
    <div className="relative w-full h-full">
      <div
        ref={containerRef}
        className="w-full h-full"
        style={{ background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)' }}
      />
      {hoveredElement && (
        <div className="absolute top-4 left-4 bg-black/80 text-white p-3 rounded-lg pointer-events-none">
          <div className="text-lg font-bold">{hoveredElement.symbol}</div>
          <div className="text-sm">{hoveredElement.name}</div>
          <div className="text-xs text-gray-300">Atomic #: {hoveredElement.atomicNumber}</div>
          <div className="text-xs text-gray-300">Mass: {hoveredElement.atomicMass.toFixed(3)}</div>
        </div>
      )}
    </div>
  );
};
