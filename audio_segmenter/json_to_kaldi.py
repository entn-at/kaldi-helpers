import json;
import sys;
import uuid;
import os;

try:
    input_json_fname = sys.argv[1];
    output_folder = sys.argv[2];
except:
    print "Invalid args";
    exit(-1);


f_in = open(input_json_fname, "r");
json_transcripts = json.loads(f_in.read());
f_in.close();

speakers = {};
recordings = {};
utterances = {};

os.makedirs(output_folder);

f_segments = open(output_folder + "/segments", "w");
f_transcripts = open(output_folder + "/transcripts", "w");
f_speakers = open(output_folder + "/spk2gender", "w");
f_recordings = open(output_folder + "/wav.scp", "w");
f_utt2spk = open(output_folder + "/utt2spk", "w");

for json_transcript in json_transcripts:
    transcript = json_transcript["transcript"];
    startMs = json_transcript["startMs"];
    stopMs = json_transcript["stopMs"];
    speakerId = json_transcript["speakerId"];
    audioFileName = json_transcript["audioFileName"].replace("\\", "/");

    if speakerId not in speakers:
        speakers[speakerId] = str(uuid.uuid4()); # create speaker id
        f_speakers.write(speakers[speakerId] + " " + "f\n"); # writing gender

    if audioFileName not in recordings:
        recordings[audioFileName] = str(uuid.uuid4()); # create recording id
        f_recordings.write(recordings[audioFileName] + " " + audioFileName + "\n");

    speaker_id = speakers[speakerId];
    recording_id = recordings[audioFileName];
    utterance_id = speakers[speakerId] + "-" + str(uuid.uuid4());

    f_transcripts.write(utterance_id + " " + transcript + "\n");
    f_segments.write(utterance_id + " " + recording_id + " " + "%f %f\n" % (startMs / 1000.0, stopMs / 1000.0));
    f_utt2spk.write(utterance_id + " " + speaker_id + "\n");


f_segments.close();
f_transcripts.close();
f_speakers.close();
f_recordings.close();
f_utt2spk.close();