import csv
class Speed:

    def __init__(self):
       self.correct_words = None
       self.accuracy = None
       self.display_word = ""
       self.display_word_user = ""
       self.user_text = ""
       self.temp_text = ""
       self.wpm = 0
       self.time = 0
       self.total_words = None


    @staticmethod
    def read_csv(csv_file_path:str):
        words = []
        with open(csv_file_path, "r") as f:
            reader = csv.reader(f)
            for word in reader:
                words.append(word[0])
        return words

    def clear_all_values(self):
        self.correct_words = None
        self.accuracy = None
        self.display_word = ""
        self.display_word_user = ""
        self.user_text = ""
        self.temp_text = ""
        self.wpm = 0
        self.time = 0
        self.total_words = None

    @staticmethod
    def set_text(sentence_list):
        sentence = ""
        for idx in range(len(sentence_list)):
            if idx < len(sentence_list) - 1:

                sentence += f"{sentence_list[idx]} "
            else:

                sentence += f"{sentence_list[idx]}"
        return sentence


    def check_user_typed(self,user_typed_text,ui):

        # user_typed_text = user_typed_text.replace("  "," * ").split()
        user_typed_text = user_typed_text.replace(" ","").split()
        # print(user_typed_text)
        text = self.display_word.split()
        total_words = len(user_typed_text)

        if self.temp_text == "":
            self.wpm=0
            self.accuracy = 0
            self.correct_words = 0
        count = 0
        skipped = []
        word_count = 1

        for index in range(total_words):

            try:
                if self.temp_text == "" and user_typed_text[index] == text[index]:
                    self.correct_words += 1
                user_word_len = len(user_typed_text[index])
                txt_word_len = len(text[index])
            except:
                break
            for alpa_id in range(user_word_len):
                if text[index] in skipped:
                    break
                if user_typed_text[index][alpa_id] != "*":
                    # print(f"current index {index}")

                    # print(f"user typed:{user_typed_text[index][alpa_id]},count:{count},To check: {text[index][alpa_id]}")
                    try:

                        if user_typed_text[index][alpa_id] == text[index][alpa_id]:

                            # print(f"correct: {user_typed_text[index][alpa_id]}")
                            ui(count,"green")
                            count += 1
                            word_count+=1
                            if self.temp_text == "" and word_count == 5:
                                self.wpm+=1
                                word_count=1
                        else:
                            if user_typed_text[index][alpa_id].lower() == text[index][alpa_id].lower():
                                ui(count,"blue")
                                count += 1
                            else:
                                # print(f"Wrong:  {user_typed_text[index][alpa_id]}")
                                ui(count, "red")
                                count+=1
                    except:
                        count-=txt_word_len
                        for _ in range (txt_word_len):
                            ui(count, "orange")
                            count+=1
                else:
                    for ad in range(txt_word_len):
                        ui(count, "grey")
                        count += 1
                    skipped.append(text[index])
                    # print(f"current count{count}, skipped: {skipped}")

            if user_word_len >= txt_word_len:
               pass
            else:
                if user_typed_text[index][0] !="*":
                    for ad in range(txt_word_len - user_word_len):
                        ui(count, "grey")
                        count += 1

            count += 1

    def round_wpm(self):

        wpm = round((self.wpm / 5) / self.time, 1)
        return wpm

    def accuracy_(self):
        self.accuracy = round((self.correct_words / self.total_words) * 100, 2)
        return self.accuracy

    def record(self,username:str):
        if self.correct_words is not None:

            condition = True
            data = {
                "username":username,
                    "wpm":self.round_wpm(),
                    "accuracy":self.accuracy_(),
                    "correct_words":self.correct_words
                    }
            try:

                with open("record.csv","r") as dic:
                    reader = csv.DictReader(dic)
                    for row in reader:
                        wpm = float(row["wpm"])
                        if wpm >= self.round_wpm():
                            condition = False
            except:
                pass
            if condition:
                with open("record.csv","w") as csv_file:
                    file_name=["username","wpm","accuracy","correct_words"]
                    writer = csv.DictWriter(csv_file,fieldnames=file_name)
                    writer.writeheader()
                    writer.writerow(data)

    @staticmethod
    def get_score():
        try:
            with open("record.csv","r") as score:
                data = csv.DictReader(score)
                for row in data:
                    username = row["username"]
                    wpm = row["wpm"]
                    accuracy = row["accuracy"]
                    correct_word = row["correct_words"]
                user=[username,wpm,accuracy,correct_word]

                return user
        except:
            return False