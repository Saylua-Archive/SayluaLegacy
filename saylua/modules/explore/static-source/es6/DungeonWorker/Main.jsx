/* eslint {'no-undef': 0} */
import { scriptWorker } from "../Dungeon/Core/worker";

// Must be written exactly this way in order to work.
onmessage = scriptWorker;
