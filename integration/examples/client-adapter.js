/** Reference only: import after app.js is loaded. These backend URLs do not exist in the static demo.
 * No automatic wiring is enabled in index.html. The host must call this explicitly.
 * Gateway owns auth, authorization, coalescing, request cancellation and idempotency.
 */
export function attachBackend({agentUrl='/api/agent', actionUrl='/api/call-actions', onError=console.error}={}) {
  const ui=window.sentimeter;
  if(!ui) throw new Error('Wait for the Sentimeter app module to load');
  ui.setMode('live');
  async function sendAction({detail}) {
    if(detail.mode!=='live') return;
    try {
      const response=await fetch(actionUrl,{method:'POST',credentials:'same-origin',
        headers:{'Content-Type':'application/json','Idempotency-Key':detail.id},body:JSON.stringify(detail)});
      if(!response.ok) throw new Error(`Action HTTP ${response.status}`);
      const acknowledgement=await response.json();
      // Proposed ACK envelope. Backend team must agree and validate this schema.
      if(acknowledgement.callState) ui.setCallState(acknowledgement.callState);
    } catch(error) { onError(error); } // Never report success or retry side effects automatically.
  }
  window.addEventListener('sentimeter:action',sendAction);
  return {
    acceptTranscript:segment=>ui.ingestTranscript(segment),
    acceptCallState:state=>ui.setCallState(state),
    // Invoke only after final context, authorization and workflow readiness are established.
    // connectAgent reports streaming failures through sentimeter:connection-error.
    run:()=>ui.connectAgent({url:agentUrl,input:ui.getRunInput()}),
    dispose:()=>{window.removeEventListener('sentimeter:action',sendAction);ui.disconnect();}
  };
}
