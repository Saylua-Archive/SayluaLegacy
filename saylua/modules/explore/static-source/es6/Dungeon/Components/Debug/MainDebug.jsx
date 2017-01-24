import Inferno from "inferno";

export default function MainDebug(props) {
  return (
    <div className="section-general">
      <button onClick={ props.debugRegenerateDungeon }>Regenerate Dungeon</button>
      <button onClick={ props.debugRevealMap }>Reveal Dungeon</button>
    </div>
  );
}
