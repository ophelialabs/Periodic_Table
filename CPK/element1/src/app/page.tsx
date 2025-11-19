"use client";

import { CopilotSidebar } from "@copilotkit/react-ui";
import PeriodicTableViewer from "@/components/PeriodicTableViewer";

export default function CopilotKitPage() {
  return (
    <main className="w-full h-screen overflow-hidden">
      <PeriodicTableViewer />
      <CopilotSidebar
        clickOutsideToClose={false}
        defaultOpen={true}
        labels={{
          title: "Periodic Table AI Assistant",
          initial: "👋 Welcome to the Interactive Periodic Table!\n\nI'm your chemistry AI assistant. I can help you:\n\n**Explore Elements:**\n- \"Show me all transition metals\"\n- \"Find elements with electronegativity above 3\"\n- \"Select Gold and show its properties\"\n\n**Analyze Data:**\n- \"Compare atomic masses across Period 2\"\n- \"Create a chart of melting points for noble gases\"\n- \"Analyze trends in ionization energy\"\n\n**Visualizations:**\n- \"Generate a 3D visualization of atomic radius trends\"\n- \"Create a correlation matrix of element properties\"\n- \"Show me a heatmap of electronegativity by period\"\n\nTry any of these commands to get started! 🧪⚗️"
        }}
      />
    </main>
  );
}
