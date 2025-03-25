import { defineStore } from 'pinia';
import axios from 'axios';

export const useMediMateOutputStore = defineStore('medimate-output', {
    id: 'medimate-output',
    state: () => ({
        mediMateSessionOutputs: [],
        mediMateSessionOutput: {
            patientId: '',
            outputType: '',
            output: {
                summary: '',
                metrics: '',
            }
        },
    }),
    actions: {
        initStore() {
            if (localStorage.getItem('mediMateSessionOutputs')) {
                this.mediMateSessionOutputs = JSON.parse(localStorage.getItem('mediMateSessionOutputs'));
                console.log('Initalised mediMateSessionOutputs: ', this.mediMateSessionOutputs);
            }
        },
        updateMediMateSessionOutputs() {
            this.mediMateSessionOutputs.push(this.mediMateSessionOutput);
            localStorage.setItem('mediMateSessionOutputs', JSON.stringify(this.mediMateSessionOutputs));
            this.resetObject();
        },
        doesPatientExist(patientId, outputType) {
            return this.mediMateSessionOutputs.some(output => output.patientId === patientId && output.outputType === outputType);
        },
        fetchPatientRecord(patientId, outputType) {
            return this.mediMateSessionOutputs.find(output => output.patientId === patientId && output.outputType === outputType) || null;
        },
        removePatientOutputEntry(patientId, outputType) {
            const index = this.mediMateSessionOutputs.findIndex(output => output.patientId === patientId && output.outputType === outputType);
            if (index > -1) {
                this.mediMateSessionOutputs.splice(index, 1);
                localStorage.setItem('mediMateSessionOutputs', JSON.stringify(this.mediMateSessionOutputs));
            }
        },
        resetObject() {
            this.mediMateSessionOutput = {
                patientId: '',
                outputType: '',
                output: {
                    summary: '',
                }
            }
        },
        createMediMateSessionOutput(patientId, outputType, object) {
            if (this.doesPatientExist(patientId, outputType)) {
                this.removePatientOutputEntry(patientId, outputType)
            }
            this.mediMateSessionOutput.patientId = patientId;
            this.mediMateSessionOutput.outputType = outputType;
            this.mediMateSessionOutput.output.summary = object.summary;
            this.mediMateSessionOutput.output[outputType] = object[outputType];
            this.mediMateSessionOutput.output.metrics = object.evaluation;
            this.updateMediMateSessionOutputs();
        }
    },
})

// {
//     "summary": "",
//     "encounters": [
//    
//     ]
// }