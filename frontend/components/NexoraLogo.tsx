export default function NexoraLogo({ className = "w-6 h-6" }: { className?: string }) {
  return (
    <svg 
      className={className} 
      viewBox="0 0 40 40" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Circular logo with interconnected nodes/petals */}
      <circle cx="20" cy="20" r="18" stroke="currentColor" strokeWidth="1.5" fill="none" opacity="0.3" />
      
      {/* Central circle */}
      <circle cx="20" cy="20" r="3" fill="currentColor" />
      
      {/* Outer nodes/petals arranged in gear pattern */}
      {[...Array(8)].map((_, i) => {
        const angle = (i * 45) * (Math.PI / 180);
        const x = 20 + 12 * Math.cos(angle);
        const y = 20 + 12 * Math.sin(angle);
        return (
          <circle key={i} cx={x} cy={y} r="2.5" fill="currentColor" />
        );
      })}
      
      {/* Interconnecting lines */}
      {[...Array(8)].map((_, i) => {
        const angle = (i * 45) * (Math.PI / 180);
        const x = 20 + 12 * Math.cos(angle);
        const y = 20 + 12 * Math.sin(angle);
        return (
          <line 
            key={i} 
            x1="20" 
            y1="20" 
            x2={x} 
            y2={y} 
            stroke="currentColor" 
            strokeWidth="1" 
            opacity="0.4"
          />
        );
      })}
      
      {/* Connecting outer nodes */}
      {[...Array(8)].map((_, i) => {
        const angle1 = (i * 45) * (Math.PI / 180);
        const angle2 = ((i + 1) * 45) * (Math.PI / 180);
        const x1 = 20 + 12 * Math.cos(angle1);
        const y1 = 20 + 12 * Math.sin(angle1);
        const x2 = 20 + 12 * Math.cos(angle2);
        const y2 = 20 + 12 * Math.sin(angle2);
        return (
          <line 
            key={`outer-${i}`} 
            x1={x1} 
            y1={y1} 
            x2={x2} 
            y2={y2} 
            stroke="currentColor" 
            strokeWidth="1" 
            opacity="0.3"
          />
        );
      })}
    </svg>
  );
}

