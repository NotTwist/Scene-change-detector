import csv
import os
import argparse
import sys
import traceback
from contextlib import contextmanager


class TestDirectoryNotFoundError(FileNotFoundError):
    pass


def test_video_cut(dataset_path, video_info):
    try:
        # Загружаем видео, его длину и смены сцен
        frames = read_video(os.path.join(dataset_path, video_info['source']))
        video_len = video_info['len']
        true_scene_changes = load_json_from_file(os.path.join(dataset_path, video_info['scene_change']))

        # Составляем список сцен, которые не будут тестироваться
        not_use_frames = set()
        for type_scene_change in ['trash', 'fade', 'dissolve']:
            for bad_scene_range in true_scene_changes.get(type_scene_change, []):
                not_use_frames.update(list(range(bad_scene_range[0], bad_scene_range[1] + 1)))

        predicted_scene_changes, _, _ = scene_change_detector(frames)

        score = f1_score(
            true_scene_changes['cut'],
            predicted_scene_changes,
            video_len,
            not_use_frames
        )

        results = (score, 'OK')

    except:
        results = (0, f'RE: {traceback.format_exception(*sys.exc_info())}')

    return results


def run_tests(dataset_path):
    video_dataset = load_json_from_file(os.path.join(dataset_path, 'info.json'))
    video_info = video_dataset[0]  # Each video stored in separate test

    results = test_video_cut(dataset_path, video_info)

    return tuple((results, ))


def save_results(results, filename):
    header = ['f1_score', 'conclusion']
    with open(filename, 'w', newline='') as resfile:
        writer = csv.writer(resfile)
        writer.writerow(header)
        resfile.flush()
        for row in results:
            writer.writerow(row)
            resfile.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing script')
    parser.add_argument('--test_dir', type=str, default='test_files')
    parser.add_argument('--output_file', type=str, default='results.csv')

    args = parser.parse_args()

    try:
        results = run_tests(args.test_dir)
    except TestDirectoryNotFoundError as e:
        print('Failed to find test directory')
        print(e)
        sys.exit()

    save_results(results, args.output_file)
    print('Results saved to: {}'.format(args.output_file))

